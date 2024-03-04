import pyttsx3 #type: ignore
global engine
engine = pyttsx3.init()


def ttsSay(message):
       engine.say(message)
       engine.runAndWait()
       return