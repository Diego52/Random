import speech_recognition as sr 
import pyaudio as pa

r = sr.Recognizer()

with mic as source:
    audio = r.record(source)
type(audio)

r.recognize_google(audio)