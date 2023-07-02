import time
import json
import sys
import unicodedata


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

from prefix import Log  



def speech():
        command =""
        print(Log(" start hearing function"), flush=True)
        dataCom = {
                None:True
            }
        with open("main/command.json", 'w') as commands:
            json.dump(dataCom,commands)
        print(Log(" cleaned buffer command"), flush=True)
        status  = True
        while(status):
            try:
                with sr.Microphone() as source:
                    print(Log(" I'm hearing..."), flush=True)
                    voice = listener.listen(source,5,15)
                    print(Log(" send command"), flush=True)
                    command = listener.recognize_google(voice,language='it-it')
                    print(Log(" command acquired"), flush=True)
                    command = command.lower()
                    command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
                    print(Log(f" command rude acquired: {command} "), flush=True)
                    if('virgilio' in str(command)):
                        print(Log(" command speech correctly "))
                        data = {
                            command:False
                            }
                        print(Log(f" data sended - {data}"), flush=True)
                        with open("main/command.json", 'w') as comandi:
                            json.dump(data, comandi,indent=4)
                        if("spegniti" in command):
                            print(Log(" shutdown in progress"), flush=True)
                            status = False
            except:
                try:
                    if("spegniti" in command):
                            print(Log(" shutdown in progress"), flush=True)
                            status = False
                    else:
                        print(Log(" Microfono dissattivato o qualcosa è andato storto"), flush=True)                   
                        pass
                except UnboundLocalError:
                    pass
                pass
                
if __name__ == "__main__":
    speech()