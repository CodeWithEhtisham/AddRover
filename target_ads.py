import cv2
import os
import random
from deepface import DeepFace

path = os.path.dirname(os.path.abspath(__file__))


focal_length = 615  # Adjust this value based on your setup and camera focal length
actual_face_width = 14
# ads_folder = "face_and_ads/ads"
# ads_list = [os.path.join(ads_folder, f) for f in os.listdir(ads_folder)]
ads_folder = {
    "Woman":"face_and_ads/ads/man_ads.mp4",
    "Man":"face_and_ads/ads/woman_ads.mp4"
}

ads_list = list(ads_folder.values())
print(ads_list)

def calculate_distance(face_width, focal_length, actual_face_width):
    return (actual_face_width * focal_length) / face_width

cap = cv2.VideoCapture(0)
ads = cv2.VideoCapture(r"face_and_ads/ads/main_ads.mp4")

# app = QApplication(sys.argv)
# window = MainScreen()
frame_count = 0
status = True

while True:
    rett, user_frame = cap.read()
    ret, ads_frame = ads.read()
    if not ret: status = True
    print(ret)
    # print(rett, ret)
    if ret:
        user_frame = cv2.resize(user_frame, (640, 360))
        try:
            result = DeepFace.extract_faces(user_frame, detector_backend='ssd', align=True, enforce_detection=False)
            print(result)
        except Exception as e:
            print("face not detected except is running")
            result = None
            continue
        if result:
            data = result[0]['facial_area']
            x, y, w, h = data['x'], data['y'], data['w'], data['h']
            face_width = w
            distance = calculate_distance(face_width, focal_length, actual_face_width)
            if distance <= 51:
                if x and y:
                    if status:
                        gender= DeepFace.analyze(
                            img_path = user_frame,
                            actions = ['gender'],
                            detector_backend = 'ssd',
                            enforce_detection = False)[0]['dominant_gender']
                        status= False
                        ads=cv2.VideoCapture(ads_folder[gender])
                        print(gender)
                    else:
                        cv2.imshow("ads_frame",ads_frame)
                else:
                    print("face not detected if is running")
                    cv2.imshow("ads_frame", ads_frame)
            else:
                print("user is far away from camera distance is ", distance)
                cv2.imshow("ads_frame", ads_frame)
        else:
            print("face not detected else is running")

    else:
        # get random ads
        # rand = random.choice(ads_list)
        print("ads is running")
        ads = cv2.VideoCapture("face_and_ads/ads/main_ads.mp4")

    # cv2.imshow("user_frame", user_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
