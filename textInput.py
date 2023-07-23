import time
import json
import sys
import os
import unicodedata

from colorama import Fore,Back
import time

from lib.prefix import Log


with open('setting.json') as f:
    setting = json.load(f)
    
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


def text():
        command = ""
        print(Log(" start hearing function"), flush=True)
        cleanBuffer()
        status  = True
        while(status):
            command = str(input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
            if(wordActivation in command):
                print(Log(" command speech correctly "))
                copyData(command)
                if("spegniti" in command):
                    print(Log(" shutdown in progress"), flush=True)
                    status = False
            else:
                print(Log("Remember to use the key word"))
                pass
        sys.exit()
                
if __name__ == "__main__":
    text()