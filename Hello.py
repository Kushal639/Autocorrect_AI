import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def talk(text):
    engine.say(text)
    engine.runAndWait()

def list_microphones():
    microphones = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, mic_name in enumerate(microphones):
        print(f"{i}: {mic_name}")
    return microphones

def take_command(mic_index=0):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            command = command.lower()
            print(f"You said: {command}")
            return command
    except sr.WaitTimeoutError:
        print("⏰ Listening timed out while waiting for phrase to start")
        return ""
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return ""
    except sr.RequestError:
        print("⚠ Could not request results; check your internet connection")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def run_assistant():
    microphones = list_microphones()
    # Select the best mic index (change if needed)
    mic_index = 0
    print(f"Using microphone index: {mic_index}")
    
    talk("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = take_command(mic_index)
        if command == "":
            talk("I didn't catch that. Please say it again.")
            continue
        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {time}")
        elif 'play' in command:
            song = command.replace('play', '').strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        elif 'open google' in command:
            talk("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'open youtube' in command:
            talk("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif 'stop' in command or 'exit' in command or 'quit' in command:
            talk("Goodbye!")
            break
        else:
            talk("Sorry, I can only tell time, play songs, or open Google and YouTube right now.")

# ✅ Corrected main block
if __name__ == "__main__":
    run_assistant()
