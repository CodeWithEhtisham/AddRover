import asyncio
import struct
import numpy as np
import cv2
# import torch
# import asyncpg

# GPU Frame Processing
def process_frame_on_gpu(frame):
    try:
        # tensor = torch.from_numpy(frame).permute(2, 0, 1).to(torch.device("cuda"))  # HWC -> CHW format
        # tensor = tensor.float() / 255.0  # Normalize to [0, 1]
        
        # # Simulated processing (e.g., deep learning model inference)
        # result = tensor.mean(dim=0)  # Dummy operation, replace with actual model
        # return result.cpu().numpy()
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (100, 100))
        frame = cv2.Canny(frame, 100, 200)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)
        return frame
    except Exception as e:
        print(f"GPU processing error: {e}")
        return None

# Database Update
async def update_database(db_conn, result):
    try:
        # query = "INSERT INTO processed_frames (result_data) VALUES ($1)"
        # await db_conn.execute(query, result.tobytes())
        print("Database updated successfully")
    except Exception as e:
        print(f"Database update error: {e}")

# Client Handler
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected to client {addr}")

    try:
        while True:
            # Receive ad ID size
            ad_id_size_data = await reader.readexactly(4)
            ad_id_size = struct.unpack(">I", ad_id_size_data)[0]

            # Receive ad ID
            ad_id_data = await reader.readexactly(ad_id_size)
            ad_id = ad_id_data.decode()

            # Receive frame size
            frame_size_data = await reader.readexactly(4)
            frame_size = struct.unpack(">I", frame_size_data)[0]

            # Receive frame data
            frame_data = await reader.readexactly(frame_size)
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

            if frame is None:
                print(f"Received invalid frame from {addr}")
                continue

            print(f"Received frame for Ad ID: {ad_id}")

            # Process the frame on GPU
            result = process_frame_on_gpu(frame)
            if result is not None:
                await update_database(None, result)
            else:
                print("Frame processing failed.")

    except asyncio.IncompleteReadError:
        print(f"Client {addr} disconnected")
    except Exception as e:
        print(f"Unexpected error with client {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection to client {addr} closed.")


# Main Server Loop
async def main():
    try:
        server = await asyncio.start_server(handle_client, 'localhost', 12345)
        print("Server is running...")
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Unexpected server error: {e}")

asyncio.run(main())
