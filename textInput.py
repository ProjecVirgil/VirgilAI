import time
import json
import sys
import unicodedata
import time

from lib.logger import Logger
from lib.utils import Utils

# ----- File to take the input by the console -----


with open('setting.json') as f:
    setting = json.load(f)
    wordActivation = str(setting['wordActivation']).lower()


class TextInput:
    
    
    def __init__(self) -> None:
        self.dataEmpy = {
            None:True
            }
        
        
    def copyData(self,command:str):
        data = {
            command:False
            }
        print(Logger.Log(f" data sended - {data}"), flush=True)
        with open("connect/command.json", 'w') as comandi:
            json.dump(data, comandi,indent=4)

    #MAIN
    def text(self):
            command = ""
            print(Logger.Log(" start hearing function"), flush=True)
            Utils.cleanBuffer(dataEmpty=self.dataEmpy,fileName="command")
            status  = True
            while(status):
                command = str(input("Enter the command or question you need (use key word Virgilio): ")).lower()
                command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
                if(wordActivation in command):
                    print(Logger.Log(" command speech correctly "), flush=True)
                    self.copyData(command)
                    if("spegniti" in command):
                        print(Logger.Log(" shutdown in progress"), flush=True)
                        status = False
                else:
                    print(Logger.Log("Remember to use the key word"), flush=True)
                    pass
            sys.exit()
                