import speech_recognition as sr
from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def start_recording():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    return audio

def stop_and_transcribe(audio):
    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return ""

def analyze_voice(text):
    if text.strip() == "":
        return "No speech detected", 0.0

    result = sentiment_model(text)[0]
    label = result["label"]
    score = result["score"]

    depression = score if label == "NEGATIVE" else 1 - score
    return label, depression