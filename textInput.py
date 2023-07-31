import time
import json
import sys
import unicodedata
import time

from lib.logger import Logger

# ----- File to take the input by the console -----


with open('setting.json') as f:
    setting = json.load(f)
    wordActivation = str(setting['wordActivation']).lower()

def cleanBuffer():
    dataEmpty = {
                None:True
            }
    with open("connect/command.json", 'w') as commands:
            json.dump(dataEmpty,commands)
    print(Logger.Log(" cleaned buffer command"), flush=True)


def copyData(command:str):
    data = {
        command:False
        }
    print(Logger.Log(f" data sended - {data}"), flush=True)
    with open("connect/command.json", 'w') as comandi:
        json.dump(data, comandi,indent=4)

#MAIN
def text():
        command = ""
        print(Logger.Log(" start hearing function"), flush=True)
        cleanBuffer()
        status  = True
        while(status):
            command = str(input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')
            if(wordActivation in command):
                print(Logger.Log(" command speech correctly "), flush=True)
                copyData(command)
                if("spegniti" in command):
                    print(Logger.Log(" shutdown in progress"), flush=True)
                    status = False
            else:
                print(Logger.Log("Remember to use the key word"), flush=True)
                pass
        sys.exit()
                