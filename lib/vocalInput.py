import time
import json
import unicodedata

import speech_recognition as sr

from lib.logger import Logger  
from lib.utils import Utils


# ----- File to take the input by the microphone -----


# init the recognizer
listener = sr.Recognizer()

with open('setting.json') as f:
        setting = json.load(f)
        listener.operation_timeout = int(setting['operation_timeout'])
        listener.dynamic_energy_threshold = bool(setting['dynamic_energy_threshold'])
        listener.energy_threshold = int(setting['energy_threshold'])
        
        wordActivation = str(setting['wordActivation']).lower()
        
        
#TO UPDATE THE NAME
class VocalInput:

    def __init__(self) -> None:
        self.dataEmpy = {
            None:True
            }
        self.logger = Logger()
        self.utils = Utils()
    
    def copyData(self,command:str):
        data = {
            command:False
            }
        print(self.logger.Log(f" data sended - {data}"), flush=True)
        with open("connect/command.json", 'w') as comandi:
            json.dump(data, comandi,indent=4)
    #Main
    def speech(self):
            command = ""
            print(self.logger.Log(" start hearing function"), flush=True)
            self.utils.cleanBuffer(dataEmpty=self.dataEmpty,fileName="command")
            status  = True
            while(status):
                try:
                    with sr.Microphone() as source:
                        print(self.logger.Log(" I'm hearing..."), flush=True)
                        voice = listener.listen(source,5,15)
                        print(self.logger.Log(" send command"), flush=True)
                        command = listener.recognize_google(voice,language='it-it')
                        print(self.logger.Log(" command acquired"), flush=True)
                        command = command.lower()
                        command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
                        print(self.logger.Log(f" command rude acquired: {command} "), flush=True)
                        if(wordActivation in command):
                            print(self.logger.Log(" command speech correctly "), flush=True)
                            self.copyData(command)
                            if("spegniti" in command):
                                print(self.logger.Log(" shutdown in progress..."), flush=True)
                                status = False
                except:
                    try:
                        if("spegniti" in command):
                                print(self.logger.Log(" shutdown in progress"), flush=True)
                                status = False
                        else:
                            print(self.logger.Log(" Microfono dissattivato o qualcosa è andato storto"), flush=True)                   
                            pass
                    except UnboundLocalError:
                        pass
                    pass
                