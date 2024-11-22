import asyncio
import cv2
import struct

async def send_frames(server_ip='localhost', server_port=12345, fps=30):
    while True:  # Infinite loop for reconnection
        try:
            print(f"Trying to connect to {server_ip}:{server_port}...")
            reader, writer = await asyncio.open_connection(server_ip, server_port)
            print("Connected to the server")

            # Open video source (camera or video file)
            cap = cv2.VideoCapture("videos/mashoo-2023-09-28_15.45.03_online-video-cutter.com_UZMO37l.mp4")
            if not cap.isOpened():
                print("Error: Unable to open video source.")
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("No frame captured, exiting.")
                    break

                # Compress the frame
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                data = buffer.tobytes()

                # Send frame size and data
                frame_size = struct.pack(">I", len(data))
                try:
                    writer.write(frame_size + data)
                    await writer.drain()
                except (ConnectionResetError, BrokenPipeError):
                    print("Connection to server lost. Reconnecting...")
                    break  # Exit inner loop and reconnect

                # Control frame rate
                await asyncio.sleep(1 / fps)

        except ConnectionRefusedError:
            print("Connection refused. Server might be down. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        except KeyboardInterrupt:
            print("Client interrupted by user. Exiting...")
            break
        finally:
            try:
                if 'cap' in locals():  # Check if cap was initialized
                    cap.release()
                if 'writer' in locals():
                    writer.close()
                    await writer.wait_closed()
            except Exception as e:
                print(f"Error during cleanup: {e}")

# Run the client
asyncio.run(send_frames())
