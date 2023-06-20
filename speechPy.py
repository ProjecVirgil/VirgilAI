import time
import json
import sys

import speech_recognition as sr
from colorama import Fore,Back
import unicodedata

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
        with open("main/command.json", 'w') as commands:
            json.dump(dataCom,commands)
        print(Log(" cleaned buffer command"))
        status  = True
        while(status):
            try:
                with sr.Microphone() as source:
                    print(Log(" I'm hearing..."))
                    voice = listener.listen(source,5,15)
                    print(Log(" send command"))
                    command = listener.recognize_google(voice,language='it-it')
                    print(Log(" command acquired"))
                    command = command.lower()
                    command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
                    print(Log(f" command rude acquired: {command} "))
                    if('virgilio' in str(command)):
                        print(Log(" command speech correctly "))
                        data = {
                            command:False
                            }
                        print(Log(f" data sended - {data}"))
                        with open("main/command.json", 'w') as comandi:
                            json.dump(data, comandi,indent=4)
                        if("spegniti" in command):
                            print(Log(" shutdown in progress"))
                            status = False
                        sys.stdout.flush()
            except:
                sys.stdout.flush()
                try:
                    if("spegniti" in command):
                            print(Log(" shutdown in progress"))
                            status = False
                    else:
                        print(Log(" Microfono dissattivato o qualcosa è andato storto"))                    
                        pass
                except UnboundLocalError:
                    pass
                pass
                
if __name__ == "__main__":
    speech()