import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

from client import aiProcess

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = os.getenv("NEWS_API_KEY")


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def processCommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:

            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        # Let Gemini handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":

    speak("Initializing Nexas....")

    while True:

        r = sr.Recognizer()

        print("recognizing...")

        try:

            # Listen for wake word
            with sr.Microphone() as source:

                print("Listening...")

                r.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = r.recognize_google(audio)

            print("You said:", word)

            if "nexas" in word.lower() or "nexus" in word.lower():

                speak("Ya")

                # Listen for command
                with sr.Microphone() as source:

                    print("Nexas Active...")
                    print("Speak your command...")

                    r.adjust_for_ambient_noise(
                        source,
                        duration=1
                    )

                    audio = r.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=10
                    )

                command = r.recognize_google(audio)

                print("Command:", command)

                processCommand(command)

        except sr.UnknownValueError:

            print("Could not understand what you said.")

        except sr.WaitTimeoutError:

            print("Listening timed out.")

        except sr.RequestError as e:

            print("Speech recognition error:", e)

        except Exception as e:

            print("Error:", repr(e))