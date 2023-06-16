# import io
# import IPython.display as ipd
# import grpc

# import riva.client

# auth = riva.client.Auth(uri='192.168.16.10:50051')

# riva_asr = riva.client.ASRService(auth)


# path = "download1.wav"
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
# print(content)
# response = riva_asr.offline_recognize(content, config)
# asr_best_transcript = response.results[0].alternatives[0].transcript
# print("ASR Transcript:", asr_best_transcript)

# print("\n\nFull Response Message:")
# print(response)

import os
import IPython.display as ipd
import grpc
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile

import riva.client

auth = riva.client.Auth(uri='192.168.16.10:50051')
riva_asr = riva.client.ASRService(auth)

# Function to handle the audio stream callback
def audio_callback(indata, frames, time, status):
    if status:
        print("Audio callback error:", status)
    else:
        # Convert the audio data to 16-bit PCM WAV file
        with open('/home/carl/Documents/AddRover/download1.wav', "wb") as fh:
            wav.write(fh, sample_rate, indata)

        # Read the converted WAV file
        with open('/home/carl/Documents/AddRover/download1.wav', "rb") as fh:
            content = fh.read()

        # Set up a recognition request
        config = riva.client.RecognitionConfig()
        config.language_code = "en-US"
        config.max_alternatives = 1
        config.enable_automatic_punctuation = True
        config.audio_channel_count = 1

        # Perform ASR on the captured audio
        response = riva_asr.offline_recognize(content, config)
        asr_best_transcript = response.results[0].alternatives[0].transcript
        print("ASR Transcript:", asr_best_transcript)

        # Remove the temporary WAV file
        # temp_wav.close()
        # os.remove(temp_filename)

# Set the desired sample rate and duration for the audio stream
sample_rate = 16000  # Adjust as needed
duration = 5  # Adjust as needed

# Start the audio stream with the specified sample rate and duration
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=sample_rate * duration)
stream.start()

# Wait for the audio stream to complete
input("Recording in progress. Press Enter to stop...")

# Stop the audio stream
stream.stop()
stream.close()

# Clean up any resources
sd.terminate()
