import cv2
import os
from threading import Thread
import time
import random
from deepface import DeepFace
# from main_screen import MainScreen
# from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, QTimer
from PyQt5 import uic
import sys
import os
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, QTimer
from PyQt5 import uic
import sys
# import cv2
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
# import riva.client
# from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
# import riva.client.audio_io
import requests
import os

# Load the UI file
UI_FILE = 'ui/main.ui'
Ui_MainWindow, _ = uic.loadUiType(UI_FILE)
path = os.path.dirname(os.path.abspath(__file__))


focal_length = 615  # Adjust this value based on your setup and camera focal length
actual_face_width = 14
# ads_folder = "face_and_ads/ads"
# ads_list = [os.path.join(ads_folder, f) for f in os.listdir(ads_folder)]
ads_folder = {
    "Man":["face_and_ads/ads/man_ads.mp4"],
    "Woman":["face_and_ads/ads/woman_ads.mp4"],
    "Both":['face_and_ads/ads/main_ads.mp4']
}

ads_list = list(ads_folder.values())
print(ads_list)

def calculate_distance(face_width, focal_length, actual_face_width):
    return (actual_face_width * focal_length) / face_width

cap = cv2.VideoCapture(0)
ads = cv2.VideoCapture(r"face_and_ads/ads/main_ads.mp4")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'/home/carl/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms'

# app = QApplication(sys.argv)
# window = MainScreen()
frame_count = 0
status = True
analytics=[]

while True:
    
    rett, user_frame = cap.read()
    ret, ads_frame = ads.read()
    if ret and rett:
        user_frame = cv2.resize(user_frame, (640, 360))
        try:
            result =DeepFace.analyze(
                            img_path = user_frame,
                            actions = ['gender'],
                            detector_backend = 'ssd',
                            enforce_detection = True)
        except Exception as e:
            # print("face not detected except is running")
            result = None
        if result:
            for res in result:
                gender=res['dominant_gender']
                # age=res['age']
                analytics.append(
                    {
                        "gender":gender,
                        # "age":age,
                        "ads":"ads path"
                    }
                )
        cv2.imshow("ads_frame", ads_frame)

        

    else:
        man_count = sum(1 for entry in analytics if entry['gender'] == 'Man')
        woman_count = sum(1 for entry in analytics if entry['gender'] == 'Woman')
        # Randomly select an ad based on the counts
        if man_count > woman_count:
            selected_ad = random.choice(ads_folder['Man'])
        elif woman_count > man_count:
            selected_ad = random.choice(ads_folder['Woman'])
        else:
            if not ads_folder['Both']:
                selected_ad = random.choice([ads_folder['Man']+ads_folder['Woman']])
            else:
                selected_ad = random.choice(ads_folder['Both'])
        print(f"number of man ads: {man_count}")
        print(f"number of woman ads: {woman_count}")
        print(selected_ad)
        analytics=[]
        # time.sleep(2)
        ads = cv2.VideoCapture(selected_ad)

    # cv2.imshow("user_frame", user_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
