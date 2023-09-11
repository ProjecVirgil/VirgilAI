""""""
import json
import threading

from colorama import Fore
import nltk


from lib import Settings
from lib.logger import Logger
from lib.choose_command import CommandSelection
from lib.request import MakeRequests
from lib.utils import Utils


# ----- File to elaborate the input  -----

class Process:
    """
    This class is responsible for processing the user's command and returning a response from Virgil API and other APIs.
    """
    def __init__(self) -> None:
        self.data_empty = {
        "0": [None, None, True]
        }
        nltk.download('punkt')
        nltk.download('stopwords')
        self.request_maker = MakeRequests()
        self.logger = Logger()
        self.utils = Utils()
        self.command_selection = CommandSelection()
        self.settings = Settings()

        self.word_activation = self.settings.word_activation

    def update_json_value(self,key:str, new_value:bool) -> None:
        """
        This function is responsible for updating the value of a key in the json file.

        Args:
            key (str): the command 
            new_value (bool): True or false
        """
        with open("connect/command.json", 'r',encoding="utf8") as file:
            data = json.load(file)
        if key in data:
            data[key] = new_value
        else:
            print(self.logger.log(f"The key '{key}' dont exist in the file JSON."), flush=True)
        with open("connect/command.json", 'w',encoding="utf8") as file:
            json.dump(data, file, indent=4)


    def clean_command(self,command:str) -> str:
        """
        Delete the word activation and strip from the command

        Args:
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            command = str(command).split(f"{self.word_activation} ")[1].strip()
            print(self.logger.log(f" command processed: {command} "), flush=True)
            return command
        except IndexError:
            #If command contain only virgil word
            return command

    def send(self,command) -> None:
        """
        Send the command in the process file (choose_command.py) for the elaboration

        Args:
            command (str): the command to send
        """
        command = self.clean_command(command)
        print(self.logger.log(" command heard correctly"), flush=True)
        print(self.logger.log(" command in process"), flush=True)
        res = self.command_selection.send_command(command)
        print(self.logger.log(" command processed updating file with the result"), flush=True)
        with open("connect/res.json", 'w',encoding="utf8") as file:
            data = {
                "0": [command, res, False]
            }
            json.dump(data, file, indent=4)


    class EventThread(threading.Thread):
        """
        Class that manage the event of a thread

        Args:
            threading (Thread)
        """
        def __init__(self, logger):
            threading.Thread.__init__(self)
            self.daemon = True
            self.logger = logger

        def check_event(self) -> None:
            """
            Check if there is an event
            """
            print(self.logger.log("  update the reminder"), flush=True)
            with open("connect/reminder.txt", "w",encoding="utf8") as file:
                file.write("0")
            print(self.logger.log(" check the old events"), flush=True)
            # Esegue altre operazioni specifiche della funzione checkEvent()
            # Nota che qui puoi utilizzare self.logger per accedere al logger

        def run(self) -> None:
            """
            Run the function
            """
            self.check_event()

    def main(self) -> None:
        """
        Main method of the program
        """
        print(self.logger.log(Fore.GREEN + " THE ASSISTENT IS ONLINE  "), flush=True)
        self.utils.clean_buffer(data_empty=self.data_empty,file_name="res")
        print(self.logger.log(" Start check event"), flush=True)
        thread = self.EventThread(self.logger)
        thread.start()
        while True:
            with open("connect/command.json", 'r',encoding="utf8") as commands:
                command = commands.read()
                if "spegniti" in command:
                    command_to_elaborate = "virgilio spegniti"
                else:
                    command_to_elaborate = "".join(command.split('":')[0])[7:]
            if "false" in command and command != None:
                print(self.logger.log(f" command processed: {command_to_elaborate}"), flush=True)
                self.send(command_to_elaborate)
                print(self.logger.log(" updating the command"), flush=True)
                self.update_json_value(command_to_elaborate, True)
            else:
                pass
