import cv2
import os
from threading import Thread
import time
import random
from deepface import DeepFace

focal_length = 615  # Adjust this value based on your setup and camera focal length
actual_face_width = 14
ads_folder = "ads"
ads_list = [os.path.join(ads_folder, f) for f in os.listdir(ads_folder)]

def calculate_distance(face_width, focal_length, actual_face_width):
    return (actual_face_width * focal_length) / face_width

cap = cv2.VideoCapture(0)
ads = cv2.VideoCapture(ads_list[0])
ads_active = True  # Flag to track whether ads frame is currently being displayed
ads_window_created = False  # Flag to track whether ads window is created

while True:
    rett, user_frame = cap.read()
    ret, ads_frame = ads.read()
    print(rett, ret)
    if ret:
        user_frame = cv2.resize(user_frame, (640, 360))
        try:
            result = DeepFace.extract_faces(user_frame, detector_backend='ssd', align=True, enforce_detection=False)
        except KeyError:
            print("face not detected except is running")
            result = None
            continue
        if result:
            data = result[0]['facial_area']
            x, y, w, h = data['x'], data['y'], data['w'], data['h']
            face_width = w
            distance = calculate_distance(face_width, focal_length, actual_face_width)
            print(distance)
            if distance <= 51:
                color = (0, 255, 0)
                distance_text = f"Distance: {distance:.2f} cm"
                cv2.putText(user_frame, distance_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, color, 2)
                if x and y:
                    user_frame = cv2.rectangle(user_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print("user is near to camera distance is ", distance)
                    if ads_window_created:
                        cv2.destroyWindow("ads_frame")
                        ads_window_created = False
                    ads_active = False
                else:
                    print("face not detected if is running")
                    if not ads_active:
                        cv2.imshow("ads_frame", ads_frame)
                        ads_window_created = True
                        ads_active = True
                    else:
                        cv2.imshow("ads_frame", ads_frame)
            else:
                print("user is far away from camera distance is ", distance)
                if not ads_active:
                    cv2.imshow("ads_frame", ads_frame)
                    ads_window_created = True
                    ads_active = True
                else:
                    cv2.imshow("ads_frame", ads_frame)
        else:
            print("face not detected else is running")

    else:
        # get random ads
        rand = random.choice(ads_list)
        print("ads is running", rand)
        ads = cv2.VideoCapture(rand)

    # cv2.imshow("user_frame", user_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
