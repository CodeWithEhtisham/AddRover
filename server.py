import asyncio
import struct
import numpy as np
import cv2
from ultralytics import YOLO  # Requires 'ultralytics' library for YOLO models
from deepface import DeepFace as df  # Requires 'deepface' library for face recognition

# Load YOLO model (pre-trained model for person detection and tracking)
model = YOLO('yolo11s.pt')  # Use the smallest YOLOv8 model for speed
keys = ['age', 'gender']
person_data = {}
alignment_modes = [True, False]
backend_model='yolov8'
# GPU Frame Processing for Unique Person Counting

def process_frame_on_gpu(frame, tracked_ids, person_data):
    info = None
    try:
        # Run YOLO tracking inference
        results = model.track(frame, persist=True, conf=0.7, classes=[0],verbose=False)  # Track 'person' class only
        detections = results[0].boxes  # Get detected bounding boxes

        # Update tracked IDs for unique person counting
        for box in detections:
            if box.id is not None:  # Each tracked person is assigned a unique ID
                if int(box.id) not in tracked_ids:
                    crop_box = box.xyxy.numpy()[0]
                    try:
                        info = df.extract_faces(
                                            img_path = frame[int(crop_box[1]):int(crop_box[3]), int(crop_box[0]):int(crop_box[2])], 
                                            detector_backend = backend_model,
                                            align = alignment_modes[1],
                                            enforce_detection=True,
                                            )
                        # info = df.analyze(frame[int(crop_box[1]):int(crop_box[3]), int(crop_box[0]):int(crop_box[2])], actions=["age","gender"], detector_backend=backend_model)[0]
                        # if info is not None:
                        #     person_data[str(int(box.id))] = {keys[0]: info[keys[0]], keys[1]: info['dominant_gender']}
                        print(info[0]['facial_area'])
                    except Exception as e:
                        print("Face Not Detected", e)
                        
                tracked_ids.add(int(box.id))
        return results[0].plot(),tracked_ids, person_data

        # Return the updated set of unique tracked IDs
        # return tracked_ids
    except Exception as e:
        print(f"GPU processing error: {e}")
        return tracked_ids

# Client Handler
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected to client {addr}")

    # Variable to store counts and track unique IDs for each Ad ID
    ad_data = {
        "current_ad_id": None,
        "unique_person_ids": set()  # Set to track unique person IDs
    }

    person_data = {}

    try:
        while True:
            # Receive ad ID size
            ad_id_size_data = await reader.readexactly(4)
            ad_id_size = struct.unpack(">I", ad_id_size_data)[0]

            # Receive ad ID
            ad_id_data = await reader.readexactly(ad_id_size)
            ad_id = ad_id_data.decode()

            # Check if a new Ad ID is received
            if ad_id != ad_data["current_ad_id"]:
                # Print previous Ad ID and unique person count if available
                if ad_data["current_ad_id"] is not None:
                    print(f"Ad ID: {ad_data['current_ad_id']} - Unique People Count: {len(ad_data['unique_person_ids'])} - Person Data: {person_data}")

                # Reset for the new Ad ID
                ad_data["current_ad_id"] = ad_id
                ad_data["unique_person_ids"] = set()  # Clear unique person IDs

            # Receive frame size
            frame_size_data = await reader.readexactly(4)
            frame_size = struct.unpack(">I", frame_size_data)[0]

            # Receive frame data
            frame_data = await reader.readexactly(frame_size)
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                print(f"Received invalid frame from {addr}")
                continue

            print(f"Processing frame for Ad ID: {ad_id}")

            # Process the frame on GPU and update unique person IDs
            frame , ad_data["unique_person_ids"], person_data = process_frame_on_gpu(frame, ad_data["unique_person_ids"], person_data)
            cv2.imshow("Processed Frame", frame)
            cv2.waitKey(1)

    except asyncio.IncompleteReadError:
        print(f"Client {addr} disconnected")
    except Exception as e:
        print(f"Unexpected error with client {addr}: {e}")
    finally:
        # Print final count for the last Ad ID before closing
        if ad_data["current_ad_id"] is not None:
            print(f"Ad ID: {ad_data['current_ad_id']} - Unique People Count: {len(ad_data['unique_person_ids'])}")

        writer.close()
        await writer.wait_closed()
        print(f"Connection to client {addr} closed.")


# Main Server Loop
async def main():
    try:
        server = await asyncio.start_server(handle_client, '127.0.0.1', 12345)
        print("Server is running on this ip :",server.sockets[0].getsockname())
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Unexpected server error: {e}")

asyncio.run(main())
