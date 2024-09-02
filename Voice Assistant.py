import sys
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

# Initialize the recognizer and the engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"
    return f"{greet} I am your Voice Assistant. How can I help you today?"

def take_command():
    """Listen for user commands and convert them to text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-US')
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
        return ""

def tell_time():
    """Tell the current time."""
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {time}")
    return f"The current time is {time}"

def tell_date():
    """Tell the current date."""
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {date}")
    return f"Today's date is {date}"

def search_wikipedia(query):
    """Search Wikipedia for a query."""
    try:
        speak("Searching Wikipedia...")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Disambiguation error: {str(e)}")
        return str(e)
    except wikipedia.exceptions.PageError as e:
        speak(f"Page error: {str(e)}")
        return str(e)
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
        return str(e)

def open_browser(query):
    """Perform a web search in Google Chrome."""
    url = f"https://www.google.com/search?q={query}"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    try:
        subprocess.Popen([chrome_path, url])
        response = f"Searching for {query} on the web."
    except FileNotFoundError:
        response = "Chrome executable not found. Please check the path."
    except Exception as e:
        response = f"Failed to open browser. Error: {str(e)}"
    
    return response

def handle_command(command):
    """Process the command and return the response."""
    if 'hello' in command or 'hi' in command:
        response = "Hello! How can I assist you?"
    elif 'time' in command:
        response = tell_time()
    elif 'date' in command:
        response = tell_date()
    elif 'wikipedia' in command:
        speak("What should I search on Wikipedia?")
        topic = take_command()
        if topic:
            response = search_wikipedia(topic)
        else:
            response = "I didn't get that. Please try again."
    elif 'search' in command:
        speak("What should I search for?")
        query = take_command()
        if query:
            response = open_browser(query)
        else:
            response = "I didn't get that. Please try again."
    elif 'exit' in command or 'quit' in command or 'stop' in command:
        response = "Goodbye! Have a nice day."
        speak(response)
        return response
    else:
        response = "I can assist with time, date, Wikipedia search, and web search. What would you like to do?"

    speak(response)
    return response

class VoiceAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Assistant")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

        # Timer to continuously check for commands
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_command)
        self.timer.start(5000)  # Check every 5 seconds

    def initUI(self):
        # Create widgets
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.speak_button = QPushButton('Speak', self)
        self.speak_button.clicked.connect(self.on_speak_button_click)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.speak_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Greet the user
        self.text_edit.append(greet_user())

    def process_command(self):
        """Continuously listen for commands and process them."""
        command = take_command()
        if command:
            response = handle_command(command)
            self.text_edit.append(f"Command: {command}\nResponse: {response}\n")

    def on_speak_button_click(self):
        """Handle the button click event."""
        self.process_command()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = VoiceAssistantApp()
    mainWin.show()
    sys.exit(app.exec_())
