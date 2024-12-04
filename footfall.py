import cv2
from ultralytics import YOLO
import os

# Load the YOLOv8 model
model = YOLO("yolov8m.pt")

# Load age and gender detection models
faceProto = "opencv_models/opencv_face_detector.pbtxt"
faceModel = "opencv_models/opencv_face_detector_uint8.pb"
ageProto = "opencv_models/age_deploy.prototxt"
ageModel = "opencv_models/age_net.caffemodel"
genderProto = "opencv_models/gender_deploy.prototxt"
genderModel = "opencv_models/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load networks for age and gender detection
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

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

def get_age_gender(face_img):
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

    # Gender prediction
    genderNet.setInput(blob)
    gender_preds = genderNet.forward()
    gender = genderList[gender_preds[0].argmax()]

    # Age prediction
    ageNet.setInput(blob)
    age_preds = ageNet.forward()
    age = ageList[age_preds[0].argmax()]

    return gender, age

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

                    # Calculate the center bottom point of the bounding box
                    bottom_center_y = y2

                    # Check if the bottom of the bounding box intersects with the virtual line and if it has not been counted
                    if bottom_center_y >= line_position and track_id not in counted_ids:
                        # Extract face ROI
                        face_img = frame[y1:y2, x1:x2]
                        gender, age = get_age_gender(face_img)

                        # Increment the total count
                        total_count += 1
                        counted_ids.add(track_id)  # Mark this object as counted

                        # Print gender, age, and update count
                        print(f"Count: {total_count}, ID: {track_id}, Gender: {gender}, Age: {age}")

                        # Write the updated count to the text file
                        write_count(total_count)

                    # Draw the bounding box and the gender/age label
                    label = f"ID: {track_id}, Gender: {gender}, Age: {age}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Annotate the frame with the current count
        cv2.putText(frame, f"Count: {total_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking with Age and Gender Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
