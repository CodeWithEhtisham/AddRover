import cv2
from ultralytics import YOLO
# Load the YOLOv8 model
model = YOLO('yolo11n.pt')

# Open the video file
video_path = "street.mp4"
cap = cv2.VideoCapture(video_path)

# Export the model
# model.export(format="engine")
# # Camera parameters (example values, you need to calibrate your camera to get actual values)

# # Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True,conf=0.5, classes=[0],device='cpu',verbose=False)  # Assuming class 0 is the object of interest

        for result in results:  
            print(result.boxes)
        #     for detection in result.boxes:
        #         # Get the bounding box coordinates
        #         print(detection)
        #         x1, y1, x2, y2 = map(int, detection.xyxy[0])

        # # Visualize the results on the frame
        # annotated_frame = results[0].plot()

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

