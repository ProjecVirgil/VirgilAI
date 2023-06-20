import time
import json
import sys

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
        command =""
        print(Log(" start hearing function"))
        dataCom = {
                None:True
            }
        with open("main/command.json", 'w') as command:
            json.dump(dataCom,command)
        print(Log(" cleaned buffer command"))
        while(True):
            try:
                with sr.Microphone() as source:
                    print(Log(" I'm hearing..."))
                    voice = listener.listen(source,5,15)
                    print(Log(" send command"))
                    command = listener.recognize_google(voice,language='it-it')
                    print(Log(" command acquired"))
                    command = command.lower()
                    print(Log(f" command rude acquired: {command} "))
                    if('virgilio' in str(command)):
                        print(Log(" command speech correctly "))
                        listaWord = command.split(" ")
                        for parola in listaWord:
                            if("'\'" in listaWord):
                                parola = " "
                        command = " ".join(listaWord)
                        data = {
                            command:False
                            }
                        print(Log(f" data sended - {data}"))
                        with open("main/command.json", 'w') as comandi:
                            json.dump(data, comandi,indent=4)
                        if("spegniti" in command):
                            sys.exit(0)
                        sys.stdout.flush()
            except:
                sys.stdout.flush()
                '''try:
                    if("spegniti" in command):
                            print(Log(" shutdown in progress"))
                            sys.exit(0)
                    else:
                        print(Log(" Microfono dissattivato o qualcosa è andato storto"))                    
                        pass
                except UnboundLocalError:
                    pass'''
                pass
                
if __name__ == "__main__":
    speech()