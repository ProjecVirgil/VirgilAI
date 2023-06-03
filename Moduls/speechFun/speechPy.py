import time

import speech_recognition as sr
from colorama import Fore,Back

from prefix.creation import Log
# init the recognizer
listener = sr.Recognizer()

#GLOBAL setting the recognizer
listener.operation_timeout = 3.0
listener.dynamic_energy_threshold=True

#SETTING FOR HEADPHONE 
listener.energy_threshold = 3500

#SETTING FOR SPEAKERS
#listener.energy_threshold = 1000


def speech():
    try:
        with sr.Microphone() as source:
            print(Log(" sto sentendo..."))
            voice = listener.listen(source,5,15)
            print(Log(" invio comando"))
            command = listener.recognize_google(voice,language='it-it')
            print(Log(" comando acquisito"))
            command = command.lower()
            print(Log(f" comando grezzo acquisito: {command} "))
            return command
    except:
            print(Log(" Microfono dissattivato o qualcosa è andato storto"))
            pass