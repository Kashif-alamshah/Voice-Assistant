import speech_recognition as sr
import pyttsx3
import streamlit as st

r=sr.Recognizer()

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        st.write("Listening:")
        audio = r.listen(source)
    try:
        user_input = r.recognize_google(audio)
        st.write("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand the audio.")
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        st.write("Could not request results from Google Speech Recognition service.")
        return "Could not request results from Google Speech Recognition service."