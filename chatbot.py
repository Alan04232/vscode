# jarvis_wo_mic.py
# Linux-friendly Jarvis using WO Mic (Bluetooth phone microphone)
# Requires: SpeechRecognition, pyttsx3

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import time
from pathlib import Path
import sys

# ---------- Text-to-Speech ----------
def init_tts(prefer_female=True, rate=170):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    voice_index = 1 if prefer_female and len(voices) > 1 else 0
    try:
        engine.setProperty("voice", voices[voice_index].id)
    except Exception:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", rate)
    return engine

engine = init_tts()

def speak(text):
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

# ---------- List available microphones ----------
def list_mics():
    print("Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {name}")

# ---------- Listen using WO Mic ----------
def take_command(r, mic_index, timeout=5, phrase_time_limit=7):
    try:
        with sr.Microphone(device_index=mic_index) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        query = r.recognize_google(audio, language="en-in")
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Recognition error:", e)
        return ""
    except Exception as e:
        print("Microphone error:", e)
        typed = input("Fallback - type your command: ")
        return typed.lower()

# ---------- Main assistant ----------
def main():
    r = sr.Recognizer()
    speak("Starting assistant.")
    time.sleep(0.5)
    wish_user()

    # Linux-compatible music folder
    music_dir = Path.home() / "Music"

    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break, and it said: 'No problem — I'll go to sleep.'"
    ]

    # Optional: uncomment to see all mic devices
    # list_mics()

    # Replace with the device index of your WO Mic
    mic_index = 3

    while True:
        query = take_command(r, mic_index)
        if not query:
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
            if music_dir.is_dir():
                songs = [f for f in os.listdir(music_dir) if os.path.isfile(music_dir / f)]
                if songs:
                    song = random.choice(songs)
                    speak(f"Playing {song}")
                    try:
                        os.system(f'xdg-open "{music_dir / song}"')
                    except Exception as e:
                        print("Error opening file:", e)
                        speak("Unable to play music file.")
                else:
                    speak("No music files found in your music folder.")
            else:
                speak("Music folder path is invalid.")

        elif "joke" in query:
            speak(random.choice(jokes))

        elif "who are you" in query or "your name" in query:
            speak("I am Jarvis, your Python voice assistant.")

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
