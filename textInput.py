import time
import json
import sys
import os
import unicodedata

from colorama import Fore,Back
import time


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
            command = str(input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command).encode('ascii', 'ignore').decode('ascii')

            if('virgilio' in str(command)):
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
            else:
                print(Log("Remember to use the key word"))
                pass
                            
        sys.exit()
                
if __name__ == "__main__":
    speech()