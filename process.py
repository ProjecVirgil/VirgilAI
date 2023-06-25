import json
import sys
import time
import threading
import requests
import calendar
import datetime
import threading

import openai
from colorama import Fore,Back
import speech_recognition as sr
from googletrans import Translator

#from prefix.creation import Log
from Moduls.CalendarRec import Recoverycalendar
from Moduls.timeConv import TimeConversion
from Moduls.ChooseCommand import SendCommand


import speech_recognition as sr
from colorama import Fore,Back

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

  


def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("main/command.json", 'r') as file:
        data = json.load(file)

    # Modifica il valore desiderato
    if key in data:
        data[key] = new_value
    else:
        print(Log(f"The key '{key}' dont exist in the file JSON."), flush=True)

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("main/command.json", 'w') as file:
        json.dump(data, file, indent=4)

def clean(command):
        #Cancellation element before the key word
        try:
            command = str(command).split("virgilio ")[1].strip()
            print(Log(f" command processed: {command} "), flush=True)
            return command
        except IndexError:
            return command


def invio(command:str):
        command = clean(command)
        print(Log(" command heard correctly"), flush=True)
        print(Log(" command in process"), flush=True)
        res = SendCommand.command(command)
        print(Log(" command processed updating file with the result"), flush=True)
        with open("main/res.json", 'w') as file:
            data = {
                "0":[command,res,False]
            }
            json.dump(data,file,indent=4)
        
        

def main():
    print(Log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "), flush=True)
    dataRes = {
                "0":[None,None,True]
            }
    with open("main/res.json", 'w') as res:
        json.dump(dataRes,res)
    print(Log(" cleaned buffer result"), flush=True)
    #starting phrase
    while(True):
        with open("main/command.json", 'r') as comandi:
            command = comandi.read()
            if("spegniti" in command):
                commandLav = "virgilio spegniti"
            else:    
                commandLav = "".join(command.split(":")[0])[7:-1]
        if("false" in command and command != None):
            print(Log(f" command processed: {commandLav}"), flush=True)
            thread_processo = threading.Thread(target=invio(commandLav))
            thread_processo.start()
            thread_processo.join()
            print(Log(f" updating the command"), flush=True)
            update_json_value(commandLav, True)
        else:
            pass
            
        
        

    
if __name__ == "__main__":
    # Creazione dei thread
    thread_ascolto = threading.Thread(target=main)
    # Avvio dei thread
    thread_ascolto.start()
    # Attendi che i thread terminino (in realtà, il thread di ascolto continuerà a eseguirsi in background)
    thread_ascolto.join()
    
    
    
    