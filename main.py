import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

newsapi = os.getenv("NEWSAPI_KEY")

# Initialize TTS engine (optional - comment out if not working)
# engine = pyttsx3.init()

def speak(text):
    print(f"Jarvis: {text}")
    # engine.say(text)
    # engine.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

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
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 





def get_text_input():
    """Get command via text input"""
    print("\n--- Type your command (or 'quit' to exit) ---")
    return input("You: ")

def get_voice_input(r):
    """Get command via voice input"""
    print("Listening for wake word 'Jarvis'...")
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
        word = r.recognize_google(audio)
        if word.lower() == "jarvis":
            speak("Yes?")
            print("Jarvis Active... (say your command)")
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=10)
            command = r.recognize_google(audio)
            return command
    except Exception as e:
        print(f"Voice error: {e}")
    return None

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    print("\n=== Jarvis Voice Assistant ===")
    print("Choose input method:")
    print("1. Voice input (say 'Jarvis' to activate)")
    print("2. Text input (type your commands) - RECOMMENDED")

    try:
        mode = input("Enter 1 or 2 (default: 2): ").strip()
    except EOFError:
        mode = "2"

    if mode == "2" or mode == "":
        # Text input mode (default)
        speak("Switching to text mode")
        while True:
            command = get_text_input()
            if command.lower() == "quit":
                speak("Goodbye!")
                break
            if command.strip():
                print(f"Processing: {command}")
                processCommand(command)
    else:
        # Voice input mode
        speak("Voice mode activated")
        while True:
            r = sr.Recognizer()
            try:
                command = get_voice_input(r)
                if command:
                    processCommand(command)
            except Exception as e:
                print(f"Error: {e}")


