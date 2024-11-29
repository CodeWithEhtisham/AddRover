# from ultralytics import YOLO
# from ultralytics.solutions import object_counter
# import cv2

# model = YOLO("yolo_models/yolov8n.pt")
# cap = cv2.VideoCapture(0)
# assert cap.isOpened(), "Error reading video file"
# w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# # line_points = [(20, 400), (1080, 400)]  # line or region points
# # classes_to_count = [0]  # person 

# # Video writer
# # video_writer = cv2.VideoWriter("object_counting_output.avi",
# #                        cv2.VideoWriter_fourcc(*'mp4v'),
# #                        fps,
# #                        (w, h))

# # Init Object Counter
# # counter = object_counter.ObjectCounter()
# # counter.set_args(view_img=True,
# #                  reg_pts=line_points,
# #                  classes_names=model.names,
# #                  draw_tracks=True)

# while cap.isOpened():
#     success, im0 = cap.read()
#     if not success:
#         print("Video frame is empty or video processing has been successfully completed.")
#         break
#     # tracks = model.track(im0, persist=True, show=False,
#     #                      classes=asses_to_countcl)
#     tracks = model.track(im0, persist=True, show=False,
#                          classes=[0])
    
#     # im0 = counter.start_counting(im0, tracks)
#     # video_writer.write(im0)
#     # cv2.imshow("Frame", im0)

# cap.release()
# # video_writer.release()
# cv2.destroyAllWindows()

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolo11m.pt')

# Open the video file
video_path = "street.mp4"
cap = cv2.VideoCapture(video_path)

# Camera parameters (example values, you need to calibrate your camera to get actual values)
KNOWN_WIDTH = 0.2  # Known width of the object in meters (e.g., 20 cm)
FOCAL_LENGTH = 800  # Focal length of the camera in pixels (this is an example value)

def calculate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes=[0])  # Assuming class 0 is the object of interest

        for result in results:
            for detection in result.boxes:
                # Get the bounding box coordinates
                x1, y1, x2, y2 = map(int, detection.xyxy[0])

                # Calculate the width of the bounding box in pixels
                box_width = x2 - x1

                # Calculate the distance to the object
                distance = calculate_distance(KNOWN_WIDTH, FOCAL_LENGTH, box_width)

                # Annotate the frame with distance information on the top-right corner of the bounding box
                cv2.putText(frame, f"Distance: {distance:.2f} m", (x2, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

