from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5 import uic
import sys
import cv2
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
import riva.client.audio_io
import requests
from PyQt5.QtCore import QTimer
# Load the UI file
UI_FILE = 'ui/main.ui'
Ui_MainWindow, _ = uic.loadUiType(UI_FILE)


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
            16000,
            4000,  # Make sure this number fits your needs
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
        self.video_path = "/home/carl/Documents/AddRover/videos/aladdin-and-the-king-of-thieves-genie.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

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
        # show video widget in the qframe


        self.api_url = "http://127.0.0.1:5000/api"
        self.pending_question = ""
        self.listening = False
        self.timer = QTimer()  # Create a QTimer instance
        self.timer.setInterval(2000)  # Set the interval to 1 second (adjust as needed)
        self.timer.timeout.connect(self.on_timer_timeout)



    def handle_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.play()

    def start_listening(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = SpeechRecognitionThread()
            self.thread.recognized.connect(self.handle_recognition)
            self.thread.start()
            self.listening = True
            self.timer.start()

    def handle_recognition(self, transcription):
        print(transcription)
        # if self.listening:
        self.lineEdit.setText(transcription)

        # If the user speaks, reset the timer
        self.timer.start()

    def on_timer_timeout(self):
        print("Timer timed out.",self.timer.isActive())
        # If the timer times out (user stopped speaking), and we are still listening
        print("Timer timed out and we are still listening.", self.listening)
        if self.timer.isActive():
            # Stop listening and make the API call
            self.listening = False
            self.timer.stop()
            print("text:",self.lineEdit.text())
            # Create a JSON object with the question
            question_json = {
                "messages": self.lineEdit.text()
            }

            # Make the API call with a POST request
            # if self.lineEdit.text() != "":
            #     response = requests.post(self.api_url, json=question_json)
            #     if response.status_code==200:
            #         response_json = response.json()
            #         print(response_json)
            #         self.lineEdit.setText(response_json["response"])
            #     else:
            #         print("Error: ",response.status_code)


def main():
    app = QApplication(sys.argv)
    window = MainScreen()
    window.show()  # Open the window
    # window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
