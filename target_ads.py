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
import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
import riva.client.audio_io
import requests
import os



# Load the UI file
UI_FILE = 'ui/main.ui'
Ui_MainWindow, _ = uic.loadUiType(UI_FILE)
path = os.path.dirname(os.path.abspath(__file__))

class SpeechRecognitionThread(QThread):
    recognized = pyqtSignal(str)

    def run(self):
        uri = "192.168.16.10:50051"
        auth = riva.client.Auth(uri=uri)
        asr_service = riva.client.ASRService(auth)
        config = riva.client.StreamingRecognitionConfig(
            config=riva.client.RecognitionConfig(
                encoding=riva.client.AudioEncoding.LINEAR_PCM,
                language_code="en-US",
                max_alternatives=1,
                profanity_filter=True,
                enable_automatic_punctuation=False,
                verbatim_transcripts=True,
                sample_rate_hertz=16000,
            ),
            interim_results=True,
        )

        with riva.client.audio_io.MicrophoneStream(
            rate=16000,
            chunk=4000,  # Make sure this number fits your needs
        ) as audio_chunk_iterator:
            responses = asr_service.streaming_response_generator(
                audio_chunks=audio_chunk_iterator,
                streaming_config=config,
            )
            for response in responses:
                if response.results:
                    transcription = response.results[0].alternatives[0].transcript
                    self.recognized.emit(transcription)  # Emit the recognized signal with the transcription


class MainScreen(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.btn_mic.clicked.connect(self.start_listening)
        self.thread = None

        # Create a QMediaPlayer
        self.video_path = os.path.join(path, "animation/aladdin-and-the-king-of-thieves-genie.mp4")
        # self.cap = cv2.VideoCapture(self.video_path)

        # Create a QVideoWidget and set it as the central widget of the QFrame
        self.video_widget = QVideoWidget(self.frame_2)
        self.layout = QVBoxLayout(self.frame_2)
        self.layout.addWidget(self.video_widget)

        # Create a QMediaPlayer and set the QVideoWidget as its video output
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
        self.player.play()
        self.player.stateChanged.connect(self.handle_state_changed)

        self.api_url = "http://127.0.0.1:5000/api"
        self.pending_question = ""
        self.listening = False
        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.api_response = None  # Store the API response here

    def handle_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.play()

    def start_listening(self):
        print("start listening")
        if self.thread is None or not self.thread.isRunning():
            print("start thread if")
            self.thread = SpeechRecognitionThread()
            self.thread.recognized.connect(self.handle_recognition)
            self.thread.start()
            self.listening = True
            self.timer.start()
        else:
            print("start thread else")
            self.listening = True
            self.timer.start()

    def handle_recognition(self, transcription):
        if self.listening:
            print(transcription)
            self.lineEdit.setText(transcription)

            # If the user speaks, reset the timer
            self.timer.start()

    def on_timer_timeout(self):
        if self.timer.isActive():
            self.listening = False
            self.timer.stop()
            if self.lineEdit.text() != "":
                self.pending_question = self.lineEdit.text()  # Save the question to send to the API
                self.send_api_request()

    def send_api_request(self):
        question_json = {
            "messages": self.pending_question
        }
        print(question_json)
        # Make the API call with a POST request
        response = requests.post(self.api_url, json=question_json)
        if response.status_code == 200:
            response_json = response.json()
            result = response_json['response']
            print(result)
            self.api_response = result
            self.lineEdit.setText(result)
            QTimer.singleShot(3000, self.start_listening)  # Start listening again after 3 seconds
        else:
            print("Error: ", response.status_code)
            self.listening = True
            self.timer.start()


focal_length = 615  # Adjust this value based on your setup and camera focal length
actual_face_width = 14
# ads_folder = "face_and_ads/ads"
# ads_list = [os.path.join(ads_folder, f) for f in os.listdir(ads_folder)]
ads_folder = {
    "female":"face_and_ads/ads/millenium jewel.mp4",
    "male":"face_and_ads/ads/millenium food court.mp4"
}

ads_list = list(ads_folder.values())
print(ads_list)

def calculate_distance(face_width, focal_length, actual_face_width):
    return (actual_face_width * focal_length) / face_width

cap = cv2.VideoCapture(0)
ads = cv2.VideoCapture(r"face_and_ads/ads/Millenium mall Quetta.mp4")
ads_active = True  # Flag to track whether ads frame is currently being displayed
ads_window_created = False  # Flag to track whether ads window is created
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/home/carl/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms'

app = QApplication(sys.argv)
window = MainScreen()
frame_count = 0
while True:
    rett, user_frame = cap.read()
    ret, ads_frame = ads.read()
    print(rett, ret)
    if ret:
        user_frame = cv2.resize(user_frame, (640, 360))
        try:
            result = DeepFace.extract_faces(user_frame, detector_backend='ssd', align=True, enforce_detection=False)
        except Exception as e:
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
                # color = (0, 255, 0)
                # distance_text = f"Distance: {distance:.2f} cm"
                # cv2.putText(user_frame, distance_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, color, 2)
                # get gender of user
                if x and y:
                    gender= DeepFace.analyze(
                        img_path = user_frame,
                        actions = ['age','gender'],
                        detector_backend = 'ssd',
                        enforce_detection = False)[0]
                    print(gender)
                    ads=cv2.VideoCapture(ads_folder[gender])
                    frame_count = 0
                    user_frame = cv2.rectangle(user_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print("user is near to camera distance is ", distance)
                    # main_screen.show()
                    if ads_window_created:
                        cv2.destroyWindow("ads_frame")
                        ads_window_created = False
                    ads_active = False
                    if window.isVisible():
                        frame_count += 1
                    else:
                        window.show()
                        frame_count += 1
                else:
                    print("face not detected if is running")
                    if not ads_active:
                        cv2.imshow("ads_frame", ads_frame)
                        ads_window_created = True
                        ads_active = True
                    else:
                        cv2.imshow("ads_frame", ads_frame)
            else:
                frame_count+=1
                print("frame count########################################", frame_count)
                if frame_count > 200:
                    window.hide()
                    frame_count = 0
                if window.isVisible():
                    window.hide()
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
