from deepface import DeepFace
import cv2

# cap = cv2.VideoCapture(0)
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
]

def calculate_distance(face_width, focal_length, actual_face_width):
    return (actual_face_width * focal_length) / face_width

cap = cv2.VideoCapture(4)
focal_length = 615  # Adjust this value based on your setup and camera focal length
actual_face_width = 14  # Actual width of the face in centimeters

while True:
    ret, frame = cap.read()
    # resize frame 
    # frame.resize(640, 360)
    if ret:
        frame = cv2.resize(frame, (640, 360))
        try:
            result = DeepFace.extract_faces(frame, detector_backend = 'ssd', align = True, enforce_detection = False)
        except Exception as e:
            print(e)
            result = None
            continue
        if result:
            # check if face detected or not
            # if result[0]['facial_area'] == {}:
            data=result[0]['facial_area']
            print(data)
            # {'x': 217, 'y': 50, 'w': 258, 'h': 258}
            x,y,w,h=data['x'],data['y'],data['w'],data['h']
            # Calculate the distance from the camera using face size and focal length
            face_width = w
            distance = calculate_distance(face_width, focal_length, actual_face_width)

            # Display the distance on the frame
            if distance < 50:  # You can adjust this threshold for when to display green or red text
                color = (0, 255, 0)  # Green color for closer distance
            else:
                color = (0, 0, 255)  # Red color for farther distance

            distance_text = f"Distance: {distance:.2f} cm"
            cv2.putText(frame, distance_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, color, 2)
            # if x or y = zero then it will not draw rectangle
            if x and y:
                frame=cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            else:
                print(f"face not detected")
            cv2.imshow("frame", frame)
            # break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()

    