from  deepface import DeepFace
import cv2 
# models for face detection
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]
# models for facial recognition
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

cap = cv2.VideoCapture(0)
while True:
    ret,frame= cap.read()
    if ret == False:
        break
    results=DeepFace.analyze(
      img_path = frame,
      actions = ['age','gender'],
      detector_backend = backends[-2],
      enforce_detection = False)[0]
    # [{'age': 30, 'region': {'x': 0, 'y': 0, 'w': 640, 'h': 480}, 'gender': {'Woman': 14.219871163368225, 'Man': 85.78013181686401}, 'dominant_gender': 'Man'}]

    cv2.putText(frame, str(f"{results['age']},{results['dominant_gender']}"), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    # draw bounding box for the face
    # cv2.rectangle(frame,(results['region']['x'],results['region']['y']),(results['region']['w'],results['region']['h']),(0,255,0),2)
    cv2.imshow("Frame",frame)
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

