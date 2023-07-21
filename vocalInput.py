import time
import json
import sys
import unicodedata
import os

import speech_recognition as sr
from colorama import Fore,Back


#from prefix.creation import Log
# init the recognizer
listener = sr.Recognizer()

with open('setting.json') as f:
    setting = json.load(f)
    
    listener.operation_timeout = int(setting['Listener']['operation_timeout'])
    listener.dynamic_energy_threshold = bool(setting['Listener']['dynamic_energy_threshold'])
    listener.energy_threshold = int(setting['Listener']['energy_threshold'])
    
    wordActivation = setting['wordActivation']




from lib.prefix import Log  



def speech():
        command =""
        print(Log(" start hearing function"), flush=True)
        dataCom = {
                None:True
            }
        with open("connect/command.json", 'w') as commands:
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
                    if( str(wordActivation).lower() in str(command)):
                        print(Log(" command speech correctly "))
                        data = {
                            command:False
                            }
                        print(Log(f" data sended - {data}"), flush=True)
                        with open("connect/command.json", 'w') as comandi:
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