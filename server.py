import asyncio
import struct
import numpy as np
import cv2
from ultralytics import YOLO  # Requires 'ultralytics' library for YOLO models
from deepface import DeepFace as df  # Requires 'deepface' library for face recognition
import threading as th
from datetime import datetime
import json

# Load YOLO model (pre-trained model for person detection and tracking)
dump_data = []

with open('data.json') as file:
    dump_data = json.load(file)


model = YOLO('yolo11s.pt')  # Use the smallest YOLOv8 model for speed
person_data = {}
alignment_modes = [True, False]
backend_model='yolov8'
threads = {}
# GPU Frame Processing for Unique Person Counting

def age_gen_detect(id, frame):
    try:
        info = df.analyze(frame, actions=["age","gender"], detector_backend=backend_model)[0]
        person_data[id] = {'counted': True, 'age': info['age'], 'gender': info['dominant_gender']}

    except:
        pass


def process_frame_on_gpu(frame, tracked_ids):

    if threads != {}:
        for id, thread in threads.copy().items():
            if not thread.is_alive():
                threads.pop(id)
                print("thread destroyed")
        print(f"{len(threads.keys())} threads alive..")

    try:
        # Run YOLO tracking inference
        results = model.track(frame, persist=True, conf=0.7, classes=[0],verbose=False)  # Track 'person' class only
        detections = results[0].boxes  # Get detected bounding boxes

        # Update tracked IDs for unique person counting
        for box in detections:
            info = None
            if box.id is not None:  # Each tracked person is assigned a unique ID
                # if int(box.id) not in tracked_ids:
                str_id = str(int(box.id))
                if str_id not in person_data.keys():
                    person_data[str_id] = {'counted': False, 'age': None, 'gender': None}
                
                if not person_data[str_id]['counted']:
                    crop_box = box.xyxy.numpy()[0]
                    crop_frame = frame[int(crop_box[1]):int(crop_box[3]), int(crop_box[0]):int(crop_box[2])]
                    try:
                        info = df.extract_faces(
                                            img_path = crop_frame,
                                            detector_backend = backend_model,
                                            align = alignment_modes[1],
                                            enforce_detection=True,
                                            )[0]['facial_area']
                        if str_id not in threads.keys() and (info is not None):
                            thread = th.Thread(target=age_gen_detect, args=(str_id, crop_frame), daemon=True)
                            threads[str_id] = thread
                            thread.start()

                    except Exception as e:
                        print("Face Not Detected", e)
                    
                tracked_ids.add(int(box.id))
        print(f"Number of persons in frame: {len(tracked_ids)}, Number of threads initialized: {len(threads)}")
        return results[0].plot(),tracked_ids

        # Return the updated set of unique tracked IDs
        # return tracked_ids
    except Exception as e:
        print(f"GPU processing error: {e}")
        return tracked_ids

# Client Handler
async def handle_client(reader, writer):
    global person_data
    addr = writer.get_extra_info('peername')
    print(f"Connected to client {addr}")

    # Variable to store counts and track unique IDs for each Ad ID
    ad_data = {
        "current_ad_id": None,
        "unique_person_ids": set()  # Set to track unique person IDs
    }

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
                    data = {'ad id': ad_id,
                            'time': datetime.now().strftime("%H:%M, %d-%m-%Y"), 
                            'total persons':len(ad_data['unique_person_ids']),
                            'person data': person_data}
                    
                    dump_data.append(data)
                    with open('data.json', 'w') as file:
                        json.dump(dump_data, file)
                    print(f"Ad ID: {ad_data['current_ad_id']} - Unique People Count: {len(ad_data['unique_person_ids'])} - Person Data: {person_data}")

                # Reset for the new Ad ID
                ad_data["current_ad_id"] = ad_id
                ad_data["unique_person_ids"] = set()  # Clear unique person IDs
                person_data = {}

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
            frame , ad_data["unique_person_ids"] = process_frame_on_gpu(frame, ad_data["unique_person_ids"])
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
        server = await asyncio.start_server(handle_client, '192.168.0.101', 12345)
        print("Server is running on this ip :",server.sockets[0].getsockname())
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Unexpected server error: {e}")

asyncio.run(main())
