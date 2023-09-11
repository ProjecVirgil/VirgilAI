"""
_summary_
"""
import json
import sys
import unicodedata

from lib import Settings
from lib.logger import Logger
from lib.utils import Utils

# ----- File to take the input by the console -----

class TextInput:
    """
    Class that takes a text as an argument and returns it in lowercase, without accents or special characters.
    """
    def __init__(self) -> None:
        self.data_empty = {
            None:True
            }
        self.logger = Logger()
        self.utils = Utils()
        self.settings = Settings()

        self.word_activation = self.settings.word_activation


    def copy_data(self,command:str):
        """
        Copy data from a command line and return it as string or list of strings if needed for further processing in other functions

        Args:
            command (str): Command to copy in the file
        """
        data = {
            command:False
            }
        print(self.logger.log(f" data sended - {data}"), flush=True)
        with open("connect/command.json", 'w',encoding="utf8") as comandi:
            json.dump(data, comandi,indent=4)

    
    def text(self):
        """
        The main file for recover the command from text
        """
        command = ""
        print(self.logger.log(" start hearing function"), flush=True)
        self.utils.clean_buffer(data_empty=self.data_empty,file_name="command")
        status  = True
        while status:
            command = str(
                input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command)
            command = command.encode('ascii', 'ignore').decode('ascii')
            if self.word_activation in command:
                print(self.logger.log(" command speech correctly "), flush=True)
                self.copy_data(command)
                if "spegniti" in command:
                    print(self.logger.log(" shutdown in progress"), flush=True)
                    status = False
            else:
                print(self.logger.log("Remember to use the key word"), flush=True)
        sys.exit()
                