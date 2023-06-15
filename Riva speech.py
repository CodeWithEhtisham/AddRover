# import io
# import IPython.display as ipd
# import grpc

# import riva.client

# auth = riva.client.Auth(uri='192.168.16.10:50051')

# riva_asr = riva.client.ASRService(auth)


# path = "download.wav"
# with io.open(path, 'rb') as fh:
#     content = fh.read()
# ipd.Audio(path)


# # Set up an offline/batch recognition request
# config = riva.client.RecognitionConfig()
# #req.config.encoding = ra.AudioEncoding.LINEAR_PCM    # Audio encoding can be detected from wav
# #req.config.sample_rate_hertz = 0                     # Sample rate can be detected from wav and resampled if needed
# config.language_code = "en-US"                    # Language code of the audio clip
# config.max_alternatives = 1                       # How many top-N hypotheses to return
# config.enable_automatic_punctuation = True        # Add punctuation when end of VAD detected
# config.audio_channel_count = 1                    # Mono channel

# response = riva_asr.offline_recognize(content, config)
# asr_best_transcript = response.results[0].alternatives[0].transcript
# print("ASR Transcript:", asr_best_transcript)

# print("\n\nFull Response Message:")
# print(response)




import grpc
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

import riva.client

auth = riva.client.Auth(uri='192.168.16.10:50051')
riva_asr = riva.client.ASRService(auth)

# Set up audio stream parameters
sample_rate = 16000  # Sample rate of the audio stream
chunk_duration = 0.1  # Duration of each audio chunk in seconds

# Define callback function to process each audio chunk
def audio_callback(indata, frames, time, status):
    if status:
        print('Error:', status)
    
    # Convert audio data to bytes and convert encoding to FLAC
    audio_data = np.array(indata * 32768, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), sample_width=2, channels=1, frame_rate=sample_rate)
    audio_segment.export('temp.flac', format='flac')
    with open('temp.flac', 'rb') as f:
        audio_bytes = f.read()
    
    # Set up the recognition configuration
    config = riva.client.RecognitionConfig()
    config.language_code = "en-US"
    config.max_alternatives = 1
    config.enable_automatic_punctuation = True
    config.audio_channel_count = 1
    
    # Perform speech activity detection on the audio chunk
    is_speech = check_speech_activity(audio_data)  # Replace with your speech activity detection logic
    
    # If speech is detected, perform real-time recognition
    if is_speech:
        response = riva_asr.offline_recognize(audio_bytes, config)
        print("Sending audio chunk to Riva...")
        if response.results:
            asr_best_transcript = response.results[0].alternatives[0].transcript
            print("ASR Transcript:", asr_best_transcript)
            # Add code here to handle the response and generate a virtual assistant response
    
    # You can add your logic here to generate the virtual assistant response
    # For example, you can use a natural language understanding (NLU) library to process the transcript and generate a response

# Function to check speech activity (energy-based detection)
def check_speech_activity(audio_data):
    # Calculate the energy of the audio chunk
    energy = np.sum(np.square(audio_data))
    
    # Define a threshold value for speech detection
    threshold = 1000000  # Adjust this threshold based on your audio data
    
    # Check if the energy exceeds the threshold
    if energy > threshold:
        return True  # Speech is detected
    else:
        return False  # No speech detected


# Start streaming audio from the microphone
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=int(sample_rate * chunk_duration))
stream.start()

# Keep the stream running until user interrupts
print("Streaming started. Speak into the microphone...")
try:
    while True:
        pass
except KeyboardInterrupt:
    stream.stop()
    stream.close()
