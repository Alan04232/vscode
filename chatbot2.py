# voice_assistant_linux.py
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import time
import sys
from pathlib import Path

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

# ---------- Microphone selection ----------
def list_mics():
    p = sr.Microphone.list_microphone_names()
    for i, name in enumerate(p):
        print(f"Device {i}: {name}")

def select_mic(device_index=None):
    if device_index is not None:
        return sr.Microphone(device_index=device_index)
    # fallback to default mic
    return sr.Microphone()

# ---------- Listen to user ----------
def take_command(timeout=5, phrase_time_limit=7, mic_index=None):
    r = sr.Recognizer()
    mic_available = True
    try:
        with select_mic(mic_index) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        print("Microphone error / PyAudio not available:", e)
        mic_available = False

    if not mic_available:
        typed = input("Type your command (fallback): ")
        return typed.lower()

    try:
        print("Recognizing...")
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

# ---------- Main assistant ----------
def main():
    speak("Starting assistant.")
    time.sleep(0.5)
    wish_user()

    # Linux-compatible music folder
    music_dir = Path.home() / "Music"

    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break, and it said: 'No problem — I'll go to sleep.'"
    ]

    # Optional: print available microphones
    # list_mics()

    mic_index = 0  # change if you need another mic index

    while True:
        query = take_command(mic_index=mic_index)
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
