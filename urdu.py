# # Python program to translate
# # speech to text and text to speech


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
            
			
# 			#listens for the user's input
# 			audio2 = r.listen(source2)
			
# 			# Using google to recognize audio
# 			MyText = r.recognize_google(audio2)
# 			MyText = MyText.lower()

# 			print("Did you say ",MyText)
# 			SpeakText(MyText)
			
# 	except sr.RequestError as e:
# 		print("Could not request results; {0}".format(e))
		
# 	except sr.UnknownValueError as e:
# 		print("unknown error occurred",e)

import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Specify the microphone device index (replace with your desired index)
microphone_device_index = 0

# Loop infinitely for user to speak
while True:
    try:
        # Use the specified microphone device index as the input
        with sr.Microphone(device_index=microphone_device_index) as source2:
            print("Waiting")
            # r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Clean up")
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print("Did you say", MyText)
            SpeakText(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError as e:
        print("Unknown error occurred", e)
