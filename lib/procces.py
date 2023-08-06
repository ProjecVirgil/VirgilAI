import json
import threading
import threading

from colorama import Fore
import speech_recognition as sr

from lib.logger import Logger
from lib.chooseCommand import CommandSelection
from lib.request import MakeRequests
from lib.utils import Utils


# ----- File to elaborate the input  -----





class Process:
    
    def __init__(self) -> None:
        self.DATA_EMPTY = {
        "0": [None, None, True]
        }
        self.request_maker = MakeRequests()
        self.logger = Logger()
        self.utils = Utils()
        self.command_selection = CommandSelection()
        with open('setup/settings.json') as f:
            SETTINGS = json.load(f)
            self.WORD_ACTIVATION = str(SETTINGS['wordActivation']).lower()
    
    def update_json_value(self,key, new_value):
        # Apri il file JSON e carica i dati
        with open("connect/command.json", 'r') as file:
            data = json.load(file)
        # Modifica il valore desiderato
        if key in data:
            data[key] = new_value
        else:
            print(self.logger.Log(f"The key '{key}' dont exist in the file JSON."), flush=True)
        # Sovrascrivi il file JSON con i dati aggiornati
        with open("connect/command.json", 'w') as file:
            json.dump(data, file, indent=4)


    def cleanCommand(self,command):
        # Cancellation element before the key word
        try:
            command = str(command).split(f"{self.WORD_ACTIVATION} ")[1].strip()
            print(self.logger.Log(f" command processed: {command} "), flush=True)
            return command
        except IndexError:
            #If command contain only virgil word
            return command


    def send(self,command: str):
        command = self.cleanCommand(command)
        print(self.logger.Log(" command heard correctly"), flush=True)
        print(self.logger.Log(" command in process"), flush=True)
        res = self.command_selection.Sendcommand(command)
        print(self.logger.Log(" command processed updating file with the result"), flush=True)
        with open("connect/res.json", 'w') as file:
            data = {
                "0": [command, res, False]
            }
            json.dump(data, file, indent=4)


    class EventThread(threading.Thread):
        def __init__(self, logger):
            threading.Thread.__init__(self)
            self.daemon = True
            self.logger = logger

        def checkEvent(self):
            print(self.logger.Log("  update the reminder"), flush=True)
            with open("connect/reminder.txt", "w") as f:
                f.write("0")
            print(self.logger.Log(" check the old events"), flush=True)
            # Esegue altre operazioni specifiche della funzione checkEvent()
            # Nota che qui puoi utilizzare self.logger per accedere al logger

        def run(self):
            self.checkEvent()

    def main(self,):
        print(self.logger.Log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "), flush=True)
        self.utils.cleanBuffer(dataEmpty=self.DATA_EMPTY,fileName="res")
        print(self.logger.Log(" Start check event"), flush=True)
        t = self.EventThread(self.logger)
        t.start()
        while (True):
            with open("connect/command.json", 'r') as commands:
                command = commands.read()
                if ("spegniti" in command):
                    commandToElaborate = "virgilio spegniti"
                else:
                    commandToElaborate = "".join(command.split('":')[0])[7:]
            if ("false" in command and command != None):
                print(self.logger.Log(f" command processed: {commandToElaborate}"), flush=True)
                #TODO VERIFY IF WIHOUT THIS THE CODE WORK
                self.send(commandToElaborate)
                print(self.logger.Log(f" updating the command"), flush=True)
                self.update_json_value(commandToElaborate, True)
            else:
                pass