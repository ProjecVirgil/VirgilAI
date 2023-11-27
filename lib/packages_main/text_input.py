"""The input file for the text."""
import json
import sys
import unicodedata

from lib.packages_utility.logger import logging
from lib.packages_utility.utils import Utils


# ----- File to take the input by the console -----

def copy_data(command: str):
    """Copy data from a command line.

    and return it as string or list of strings if needed for further processing in other functions.

    Args:
        command (str): Command to copy in the file
    """
    data = {
        command: False
    }
    logging.debug(f" data sended - {data}")
    with open("connect/command.json", 'w', encoding="utf8") as comandi:
        json.dump(data, comandi, indent=4)


class TextInput:
    """Class that takes a text as an argument and returns it in lowercase, without accents or special characters."""

    def __init__(self,settings) -> None:
        """Init func.

        Args:
            settings (dataclasses): A class with some settings
        """
        self.data_empty = {
            None: True
        }
        self.utils = Utils()
        self.word_activation = settings.word_activation
        self.split_command_exit = [settings.split_command[0],settings.split_command[1]]

    def text(self):
        """The main file for recover the command from text."""
        logging.info(" start input function")
        self.utils.clean_buffer(data_empty=self.data_empty, file_name="command")
        status = True
        while status:
            command = str(
                input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command)
            command = command.encode('ascii', 'ignore').decode('ascii')
            if self.word_activation in command:
                logging.debug(" command speech correctly ")
                copy_data(command)
                if any(word in command for word in self.split_command_exit):
                    status = False
            else:
                logging.warning("Remember to use the key word")
        logging.info("Shutdown in progress from input-thread")
        sys.exit()
