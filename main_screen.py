from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame,QLabel,QDesktopWidget
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, QTimer
from PyQt5 import uic
import sys
# import cv2
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QCamera, QCameraInfo
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QImage, QPixmap

import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
import riva.client.audio_io
import requests
import os
import cv2


# Load the UI file
UI_FILE = 'ui/main.ui'
Ui_MainWindow, _ = uic.loadUiType(UI_FILE)
path = os.path.dirname(os.path.abspath(__file__))
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/home/carl/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms'
video_path = os.path.join(path, "face_and_ads/ads/millenium food court.mp4")

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

class VideoThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def run(self):
        ads = cv2.VideoCapture(video_path)  # Use appropriate camera index or video file path
        cap = cv2.VideoCapture(0)
        # Get the screen dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        while True:
            ads_ret, ads_frame = ads.read()
            ret, frame = cap.read()
            if not ads_ret and not ret:
                break
            frame = cv2.resize(frame, (640, 360))
            try:
                result=DeepFace.extractFace(frame, detector_backend='ssd', enforce_detection=False)
            except Exception as e:
                print(e)
                
            print("ads_frame",ads_frame.shape)
            # Calculate the target dimensions for resizing
            resized_frame = cv2.resize(ads_frame, (screen_width, screen_height-40))
            frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
            self.frame_signal.emit(image)



class MainScreen(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.btn_mic.clicked.connect(self.start_listening)
        self.thread = None

        # Create a QMediaPlayer
        self.video_thread = VideoThread()
        self.video_thread.frame_signal.connect(self.update_video_frame)
        self.video_thread.start()

        self.api_url = "http://192.168.16.125:5000/api"
        self.pending_question = ""
        self.listening = False
        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.api_response = None  # Store the API response here

    def update_video_frame(self, image):
        # Set the pixmap of the video_label to display the image
        self.video_frame.setPixmap(QPixmap.fromImage(image))

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

def main():
    app = QApplication(sys.argv)
    window = MainScreen()
    window.showFullScreen()
    # window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
