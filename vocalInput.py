import time
import json
import sys
import unicodedata
import os

import speech_recognition as sr
from colorama import Fore,Back


from lib.prefix import Log  





# init the recognizer
listener = sr.Recognizer()
with open('setting.json') as f:
    setting = json.load(f)
    listener.operation_timeout = int(setting['operation_timeout'])
    listener.dynamic_energy_threshold = bool(setting['dynamic_energy_threshold'])
    listener.energy_threshold = int(setting['energy_threshold'])
    
    wordActivation = str(setting['wordActivation']).lower()


def cleanBuffer():
    dataEmpty = {
                None:True
            }
    with open("connect/command.json", 'w') as commands:
            json.dump(dataEmpty,commands)
    print(Log(" cleaned buffer command"), flush=True)


def copyData(command:str):
    data = {
        command:False
        }
    print(Log(f" data sended - {data}"), flush=True)
    with open("connect/command.json", 'w') as comandi:
        json.dump(data, comandi,indent=4)

def speech():
        command = ""
        print(Log(" start hearing function"), flush=True)
        cleanBuffer()
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
                    if(wordActivation in command):
                        print(Log(" command speech correctly "))
                        copyData(command)
                        if("spegniti" in command):
                            print(Log(" shutdown in progress..."), flush=True)
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