import json
import sys
import time
import threading
import requests
import calendar
import datetime

import openai
from colorama import Fore,Back
from pyttsx3 import *
import speech_recognition as sr
from googletrans import Translator

from prefix.creation import Log
from Moduls.CalendarRec import Recoverycalendar
from  Moduls.timeConv import TimeConversion
from Moduls.speechFun import speechPy
from Moduls.ChooseCommand import SendCommand

# init the recognizer
listener = sr.Recognizer()
#GLOBAL setting the recognizer
listener.operation_timeout = 3.0
listener.dynamic_energy_threshold=True
#SETTING FOR HEADPHONE 
listener.energy_threshold = 3500

#init e setup the tts
engine = init("sapi5")
engine.setProperty("rate",180)
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
voices=engine.getProperty("voices")


def timer(my_time):
    print(Log(" timer function"))
    print(Log(" inizio timer"))
    time.sleep(my_time)
    print(Log(" fine timer"))
    engine.say("IL TIMER è FINITO")
    engine.runAndWait()
    #parte allarme
    
class TimerThread(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.daemon = True

    def run(self):
       timer(self.interval)   

def clean(command):
        #Cancellation element before the key word
        try:
            command = str(command).split("dante ")[1].strip()
            print(Log(f" comando lavorato: {command} "))
            return command
        except IndexError:
            return command

if __name__ == "__main__":
    print(Log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "))
    #starting phrase
    engine.say("Sono Dante come posso aiutarti")
    engine.runAndWait()
    while True:
        command = speechPy.speech()
        if('dante' in str(command)):
                print(Log(" comando sentito corretamente "))
                command = clean(command)
                res = SendCommand.command(command)
                if(res != None):
                    if("volume" in command):
                        engine.setProperty('volume', res)
                        engine.say("bbbiiipp")
                        engine.runAndWait()
                        print(Log(f" volume cambiato correttamente a {res*100}% "))
                    elif("timer" in command):
                        print(f"Il timer è partito ci vediamo tra {res} secondi")
                        engine.say(f"Il timer è partito ci vediamo tra {res} secondi")
                        engine.runAndWait()
                        t = TimerThread(res)
                        t.start()
                    else:
                        try:
                            engine.say(res)
                            engine.runAndWait()
                        except RuntimeError:
                            print(Log(" Evita di usare comandi subito dopo il timer"))
                            engine.runAndWait()
                            
                else:
                    print(Log(" C'è stata qualche eccezione nel codice"))
                    
        else:
                print(Log(" comando non ricevuto corretamente"))
    