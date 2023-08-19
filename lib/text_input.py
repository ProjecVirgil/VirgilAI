"""
_summary_
"""
import json
import sys
import unicodedata

from lib.logger import Logger
from lib.utils import Utils

# ----- File to take the input by the console -----

class TextInput:
    """_summary_
    """
    def __init__(self) -> None:
        self.data_empty = {
            None:True
            }
        self.logger = Logger()
        self.utils = Utils()
        with open('setup/settings.json',encoding="utf8") as file:
            settings = json.load(file)
            self.word_activation = str(settings['wordActivation']).lower()


    def copy_data(self,command:str):
        """_summary_

        Args:
            command (str): _description_
        """
        data = {
            command:False
            }
        print(self.logger.log(f" data sended - {data}"), flush=True)
        with open("connect/command.json", 'w',encoding="utf8") as comandi:
            json.dump(data, comandi,indent=4)

    #MAIN
    def text(self):
        """
        _summary_
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
                