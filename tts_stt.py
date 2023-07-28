import speech_recognition as sr
import pyaudio

def main():
    # Create a recognizer instance for speech recognition
    recognizer = sr.Recognizer()

    # Configure audio stream with PyAudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # You can adjust the sample rate to suit your needs
    audio_stream = pyaudio.PyAudio().open(format=FORMAT,
                                          channels=CHANNELS,
                                          rate=RATE,
                                          input=True,
                                          frames_per_buffer=CHUNK)

    print("Listening...")
    try:
        # Wait for a second to let the recognizer adjust the energy threshold
        recognizer.adjust_for_ambient_noise(audio_stream, duration=0.5)

        # Listen for the user's input
        audio_frames = []
        for i in range(0, int(RATE / CHUNK * 3)):  # Listen for 3 seconds
            audio_data = audio_stream.read(CHUNK)
            audio_frames.append(audio_data)

        # Perform speech recognition
        audio_data = b''.join(audio_frames)
        recognized_text = recognizer.recognize_google(audio_data, language="en-US")
        print("You said:", recognized_text)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error occurred")

    # Stop and close the audio stream
    audio_stream.stop_stream()
    audio_stream.close()
    pyaudio.PyAudio().terminate()

if __name__ == '__main__':
    main()
