
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtWidgets import QApplication
# import sys
# from os import path
# from PyQt5.uic import loadUiType

# FORM_MAIN, _ = loadUiType('ui/main.ui')


# class MainScreen(QMainWindow, FORM_MAIN):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setupUi(self)
#         self.Handle_Buttons()

#     def Handle_Buttons(self):
#         self.btn_mic.clicked.connect(self.listening)

#     def listening(self):
#         # listening from user and add text into the lineEdit
#         pass

# def main():
#     app = QApplication(sys.argv)
#     window = MainScreen()
#     window.show()
#     app.exec_()


# if __name__ == '__main__':
#     main()

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic
import sys
import argparse

import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters

import riva.client.audio_io

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

    def start_listening(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = SpeechRecognitionThread()
            self.thread.recognized.connect(self.handle_recognition)
            self.thread.start()

    def handle_recognition(self, transcription):
        print(transcription)
        self.lineEdit.setText(transcription)



def main():
    app = QApplication(sys.argv)
    window = MainScreen()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
