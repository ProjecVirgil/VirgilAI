import time
import json

import speech_recognition as sr
from colorama import Fore,Back

#from prefix.creation import Log
# init the recognizer
listener = sr.Recognizer()

#GLOBAL setting the recognizer
listener.operation_timeout = 3.0
listener.dynamic_energy_threshold=True

#SETTING FOR HEADPHONE 
listener.energy_threshold = 3500

#SETTING FOR SPEAKERS
#listener.energy_threshold = 1000


from colorama import Fore,Back
import time

def Log(string:str):
    prfx=(Fore.GREEN + time.strftime ("%H:%M:%S UTC LOG", time.localtime() )+ Back.RESET + Fore.WHITE)
    prfx = (prfx + " | ")
    log = prfx + string
    return log



def speech():
        while(True):
            try:
                with sr.Microphone() as source:
                    print(Log(" sto sentendo..."))
                    voice = listener.listen(source,5,15)
                    print(Log(" invio comando"))
                    command = listener.recognize_google(voice,language='it-it')
                    print(Log(" comando acquisito"))
                    command = command.lower()
                    print(Log(f" comando grezzo acquisito: {command} "))
                    if('dante' in str(command)):
                        print(" comando sentito corretamente ")
                        data = {
                            command:False
                            }
                        print(data)
                        with open("main/command.json", 'w') as comandi:
                            json.dump(data, comandi,indent=4)
            except:
                    print(Log(" Microfono dissattivato o qualcosa è andato storto"))                    
                    pass
                
if __name__ == "__main__":
    speech()