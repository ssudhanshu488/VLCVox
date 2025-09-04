import pvporcupine
import pyaudio
import numpy as np 
import os
import speech_recognition as sr
from openwakeword.model import Model

ACCESS_KEY = "6R/OhxFQVnlEko5OG2r33gIDSK6bbj5guXv70VLC4MhQYZAtrf9+QA=="
KEYWORD_PATH = os.path.join(os.path.dirname(__file__), "Hello-Media-Player_en_windows_v3_0_0.ppn")

def listen_for_command():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]  
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    recognizer = sr.Recognizer()
    print("Listening for wake word ('Hello Media Player')...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, phrase_time_limit=10)

                try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Recognized command: {command}")
                    return command
                except sr.UnknownValueError:
                    print("Could not understand the command.")
                    return None
                except sr.RequestError as e:
                    print(f"Recognition error: {e}")
                    return None


    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()