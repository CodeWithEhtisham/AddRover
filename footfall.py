import cv2
from ultralytics import YOLO
import os

# Load the YOLOv8 model
model = YOLO("yolov8m.pt")

# Open the video file or camera stream
video_path = 0  # Use 0 for webcam or provide the video file path
cap = cv2.VideoCapture(video_path)

# File to store the count
count_file = "counter.txt"

# Function to read the current count from the file
def read_count():
    if os.path.exists(count_file):
        with open(count_file, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    return 0

# Function to write the updated count to the file
def write_count(count):
    with open(count_file, "w") as file:
        file.write(str(count))

# Initialize the total count from the file
total_count = read_count()

# Track IDs that have been counted
counted_ids = set()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Calculate the position of the virtual line (75% of the height)
        line_position = int(0.75 * frame.shape[0])

        # Draw the virtual line on the frame
        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 255, 255), 2)

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes=[0], tracker="bytetrack.yaml", conf=0.4, iou=0.5)

        for result in results:
            for detection in result.boxes:
                # Check if detection has a valid ID
                if detection.id is not None:
                    track_id = int(detection.id[0])  # Get the track ID of the object

                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = map(int, detection.xyxy[0])

                    # Draw the bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Calculate the center bottom point of the bounding box
                    bottom_center_x = (x1 + x2) // 2
                    bottom_center_y = y2

                    # Draw a dot at the center bottom of the bounding box
                    cv2.circle(frame, (bottom_center_x, bottom_center_y), 5, (0, 0, 255), -1)

                    # Check if the bottom of the bounding box intersects with the virtual line and if it has not been counted
                    if bottom_center_y >= line_position and track_id not in counted_ids:
                        total_count += 1
                        counted_ids.add(track_id)  # Mark this object as counted

                        # Write the updated count to the text file
                        write_count(total_count)

                    # Annotate the frame with the current count
                    cv2.putText(frame, f"Count: {total_count}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
