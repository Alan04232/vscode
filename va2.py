# voice_assistant.py
# Simple Jarvis-like Voice Assistant
# Requires: SpeechRecognition, pyttsx3, pyaudio (or typed fallback)

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import time
import sys

# ---------- Text-to-Speech setup ----------
def init_tts(prefer_female=True, rate=170):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    # choose voice index (0 or 1)
    voice_index = 1 if prefer_female and len(voices) > 1 else 0
    try:
        engine.setProperty("voice", voices[voice_index].id)
    except Exception:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", rate)
    return engine

engine = init_tts()

def speak(text):
    """Speak the given text and also print to console."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ---------- Greeting ----------
def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning! I am your assistant.")
    elif hour < 18:
        speak("Good afternoon! I am your assistant.")
    else:
        speak("Good evening! I am your assistant.")
    #speak("How can I help you? You can say commands like open YouTube, what time is it, play music or stop.")

# ---------- Listen to user (with fallback to typed input) ----------
def take_command(timeout=5, phrase_time_limit=7):
    r = sr.Recognizer()
    mic_available = True
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        print("Microphone error / PyAudio not available:", e)
        mic_available = False

    if not mic_available:
        # fallback to typed input for demo if mic or PyAudio fails
        typed = input("Type your command (fallback): ")
        return typed.lower()

    try:
        print("Recognizing (uses Google Web Speech API)...")
        query = r.recognize_google(audio, language="en-in")
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; check your internet. Error:", e)
        return ""
    except Exception as e:
        print("Recognition error:", e)
        return ""

# ---------- Main assistant logic ----------
def main():
    speak("Starting assistant.")
    time.sleep(0.5)
    wish_user()

    # set this to your music folder
    music_dir = r"C:\Users\Public\Music"  # change to your folder

    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break, and it said: 'No problem — I'll go to sleep.'"
    ]

    while True:
        query = take_command()
        if not query:
            # empty → listen again
            continue

        if "time" in query:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {now}")

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query or "open browser" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif query.startswith("search "):
            term = query.replace("search", "", 1).strip()
            if term:
                speak(f"Searching for {term}")
                webbrowser.open(f"https://www.google.com/search?q={term}")
            else:
                speak("What should I search for?")

        elif "play music" in query:
            if os.path.isdir(music_dir):
                songs = [f for f in os.listdir(music_dir) if os.path.isfile(os.path.join(music_dir, f))]
                if songs:
                    song = random.choice(songs)
                    speak(f"Playing {song}")
                    try:
                        os.startfile(os.path.join(music_dir, song))
                    except Exception as e:
                        print("Error opening file:", e)
                        speak("Unable to play music file.")
                else:
                    speak("No music files found in the folder.")
            else:
                speak("Music folder path is invalid. Please update the script.")

        elif "joke" in query:
            speak(random.choice(jokes))

        elif "who are you" in query or "your name" in query:
            speak("I am Jarvis, your python voice assistant.")

        elif "exit" in query or "stop" in query or "quit" in query:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I don't know that command yet. Try 'open youtube' or 'what is the time'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
