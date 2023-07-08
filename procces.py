import json
import sys
import time
import os
import threading
import requests
import calendar
import datetime
import threading

import openai
from colorama import Fore, Back
import speech_recognition as sr
from googletrans import Translator


from lib.prefix import Log
from lib.chooseCommand import Sendcommand


# init the recognizer
listener = sr.Recognizer()

# GLOBAL setting the recognizer
listener.operation_timeout = 3.0
listener.dynamic_energy_threshold = True

# SETTING FOR HEADPHONE
listener.energy_threshold = 3500

# SETTING FOR SPEAKERS
# listener.energy_threshold = 1000


def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("connect/command.json", 'r') as file:
        data = json.load(file)

    # Modifica il valore desiderato
    if key in data:
        data[key] = new_value
    else:
        print(Log(f"The key '{key}' dont exist in the file JSON."), flush=True)

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("connect/command.json", 'w') as file:
        json.dump(data, file, indent=4)


def clean(command):
    # Cancellation element before the key word
    try:
        command = str(command).split("virgilio ")[1].strip()
        print(Log(f" command processed: {command} "), flush=True)
        return command
    except IndexError:
        return command


def invio(command: str):
    command = clean(command)
    print(Log(" command heard correctly"), flush=True)
    print(Log(" command in process"), flush=True)
    res = Sendcommand(command)
    print(Log(" command processed updating file with the result"), flush=True)
    with open("connect/res.json", 'w') as file:
        data = {
            "0": [command, res, False]
        }
        json.dump(data, file, indent=4)


def main():
    print(Log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "), flush=True)
    dataRes = {
        "0": [None, None, True]
    }
    with open("connect/res.json", 'w') as res:
        json.dump(dataRes, res)
    print(Log(" cleaned buffer result"), flush=True)
    # starting phrase
    while (True):
        with open("connect/command.json", 'r') as comandi:
            command = comandi.read()
            if ("spegniti" in command):
                commandLav = "virgilio spegniti"
            else:
                commandLav = "".join(command.split(":")[0])[7:-1]
        if ("false" in command and command != None):
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
