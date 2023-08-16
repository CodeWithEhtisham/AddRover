# Python program to translate
# speech to text and text to speech


# import speech_recognition as sr
# import pyttsx3

# # Initialize the recognizer
# r = sr.Recognizer()

# # Function to convert text to
# # speech
# def SpeakText(command):
	
# 	# Initialize the engine
# 	engine = pyttsx3.init()
# 	engine.say(command)
# 	engine.runAndWait()
	
	
# # Loop infinitely for user to
# # speak

# while(1):
	
# 	# Exception handling to handle
# 	# exceptions at the runtime
# 	try:
		
# 		# use the microphone as source for input.
# 		with sr.Microphone() as source2:
			
# 			# wait for a second to let the recognizer
# 			# adjust the energy threshold based on
# 			# the surrounding noise level

# 			print("Waiting")
# 			r.adjust_for_ambient_noise(source2, duration=0.2)
# 			print("clean up")
            
# 			print("Say Something")
# 			#listens for the user's input
#             # print("Listening");
#             # print("Listening")
# 			audio2 = r.listen(source2,timeout=5,phrase_time_limit=5)
			
# 			# Using google to recognize audio
# 			MyText = r.recognize_google(audio2)
# 			MyText = MyText.lower()

# 			print("Did you say ",MyText)
# 			SpeakText(MyText)
			
# 	except sr.RequestError as e:
# 		print("Could not request results; {0}".format(e))
		
# 	except sr.UnknownValueError as e:
# 		print("unknown error occurred",e)

# import speech_recognition as sr
# import pyttsx3

# # Initialize the recognizer
# r = sr.Recognizer()

# # Function to convert text to speech
# def SpeakText(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()

# # Specify the microphone device index (replace with your desired index)
# microphone_device_index = 3

# # Loop infinitely for user to speak
# while True:
#     try:
#         # Use the specified microphone device index as the input
#         with sr.Microphone(device_index=microphone_device_index) as source2:
#             print("Waiting")
#             # r.adjust_for_ambient_noise(source2, duration=0.2)
#             print("Clean up")
#             audio2 = r.listen(source2)
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()
#             print("Did you say", MyText)
#             SpeakText(MyText)

#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#     except sr.UnknownValueError as e:
#         print("Unknown error occurred", e)


# pip install pocketsphinx

# import speech_recognition as sr

# r = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Listening... Say something")
#     r.adjust_for_ambient_noise(source)
#     audio = r.listen(source)

# try:
#     print("Recognizing...",audio)
#     # recognized_text = r.recognize_google(audio, language="ur-PK")
#     recognized_text = r.recognize_google(audio, language="en-US")
#     recognized_text = recognized_text.lower()
#     print("You said:", recognized_text)
# except sr.UnknownValueError:
#     print("Sorry, I couldn't understand what you said.")


import deepspeech
import pyaudio

# Load the pre-trained DeepSpeech model
model_path = "deepspeech.pbmm"
ds = deepspeech.Model(model_path)

# Function to recognize speech from audio data
def recognize_speech(audio_data):
    recognized_text = ds.stt(audio_data)
    return recognized_text

# Configuration for the audio capture
chunk_size = 1024
sample_rate = 16000

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the microphone stream
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

print("Listening... Say something")

try:
    recognized_text = ""
    while True:
        audio_data = stream.read(chunk_size)
        recognized_text = recognize_speech(audio_data)
        print("You said:", recognized_text)
        
except KeyboardInterrupt:
    print("Stopping...")

# Close the microphone stream and PyAudio
stream.stop_stream()
stream.close()
audio.terminate()
