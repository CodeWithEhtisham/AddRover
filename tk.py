import tkinter as tk
from tkinter import ttk
import os
from threading import Thread
import time
import random
from deepface import DeepFace
import riva.client
from riva.client.argparse_utils import add_asr_config_argparse_parameters, add_connection_argparse_parameters
import riva.client.audio_io
import requests

# Load the UI file
UI_FILE = 'ui/main.ui'
path = os.path.dirname(os.path.abspath(__file__))

class SpeechRecognitionThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recognized = None

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
                    self.recognized = transcription  # Store the recognized transcription

class MainScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Main Screen")
        self.geometry("600x400")

        # Create a Label for the video widget
        self.video_path = os.path.join(path, "animation/aladdin-and-the-king-of-thieves-genie.mp4")
        # You will need to implement video playback in Tkinter separately

        # Create a Frame for the video widget
        self.video_frame = ttk.Frame(self)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Label and Entry for user input
        self.user_input_label = ttk.Label(self, text="User Input:")
        self.user_input_label.pack()
        self.user_input_entry = ttk.Entry(self)
        self.user_input_entry.pack()

        # Create a Button to start listening
        self.btn_mic = ttk.Button(self, text="Start Listening", command=self.start_listening)
        self.btn_mic.pack()

        self.api_url = "http://127.0.0.1:5000/api"
        self.pending_question = ""
        self.listening = False
        self.timer = None
        self.api_response = None  # Store the API response here

    def handle_recognition(self):
        if self.listening and self.timer:
            transcription = self.thread.recognized
            print(transcription)
            self.user_input_entry.delete(0, tk.END)
            self.user_input_entry.insert(0, transcription)

            # If the user speaks, reset the timer
            self.timer.start()

    def on_timer_timeout(self):
        if self.timer and self.timer.is_active():
            self.listening = False
            self.timer.stop()
            user_input = self.user_input_entry.get()
            if user_input != "":
                self.pending_question = user_input  # Save the question to send to the API
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
            self.user_input_entry.delete(0, tk.END)
            self.user_input_entry.insert(0, result)
            self.after(3000, self.start_listening)  # Start listening again after 3 seconds
        else:
            print("Error: ", response.status_code)
            self.listening = True
            self.timer.start()

    def start_listening(self):
        print("start listening")
        if not self.listening:
            print("start thread if")
            self.thread = SpeechRecognitionThread()
            self.thread.start()
            self.listening = True
            self.timer = self.after(3000, self.on_timer_timeout)
        else:
            print("start thread else")
            self.listening = True
            self.timer = self.after(3000, self.on_timer_timeout)

def main():
    window = MainScreen()
    window.mainloop()

if __name__ == '__main__':
    main()
