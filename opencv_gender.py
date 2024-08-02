import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

# Load the YOLOv8 model for face detection
model = YOLO('yolo_models/yolov8m.pt')

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

# Load network
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)

# Initialize video capture
video_path = 0  # Use 0 for webcam or provide path to video file
cap = cv2.VideoCapture(video_path)

# Create a directory to save the images
output_dir = "detected_faces"
os.makedirs(output_dir, exist_ok=True)

# Parameters
KNOWN_WIDTH = 0.2  # Known width of the object in meters (e.g., 20 cm)
FOCAL_LENGTH = 800  # Focal length of the camera in pixels (example value)
TRACKER_CONFIDENCE_THRESHOLD = 0.7  # Confidence threshold for the tracker
REIDENTIFICATION_DELAY = 30  # Frames to wait before re-identifying a person

# Storage for face tracking and age/gender prediction
tracked_faces = {}
frame_count = 0

def calculate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

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

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    
    frame_count += 1
    results = model.track(frame, persist=True, classes=[0])  # Assuming class 0 is the face class
    
    for result in results:
        for detection in result.boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            box_id = detection.id  # ID assigned by YOLOv8 tracker
            box_width = x2 - x1
            
            if box_id not in tracked_faces or (frame_count - tracked_faces[box_id]['last_seen'] > REIDENTIFICATION_DELAY):
                # Extract face ROI
                face_img = frame[y1:y2, x1:x2]
                gender, age = get_age_gender(face_img)
                
                # Save the face image with the predicted age and gender
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"{output_dir}/{timestamp}_id{box_id}_gender{gender}_age{age}.jpg"
                print("###################################")
                cv2.imwrite(filename, face_img)
                
                # Store the prediction and update the last seen frame count
                tracked_faces[box_id] = {
                    'gender': gender,
                    'age': age,
                    'last_seen': frame_count
                }
            else:
                # Update the last seen frame count for existing tracked face
                tracked_faces[box_id]['last_seen'] = frame_count
            
            # Calculate distance
            distance = calculate_distance(KNOWN_WIDTH, FOCAL_LENGTH, box_width)
            
            # Annotate the frame
            label = f"{tracked_faces[box_id]['gender']}, {tracked_faces[box_id]['age']}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Distance: {distance:.2f} m", (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Display the annotated frame
    cv2.imshow("Age Gender Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
