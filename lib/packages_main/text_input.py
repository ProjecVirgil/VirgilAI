"""The input file for the text."""
import sys
import unicodedata
import queue

from lib.packages_utility.logger import logging

# ----- File to take the input by the console -----




class TextInput:
    """Class that takes a text as an argument and returns it in lowercase, without accents or special characters."""

    def __init__(self,settings,command_queue:queue.Queue,class_manager) -> None:
        """This class is used as a wrapper around the standard input from the user in order to provide an interface that can be easily tested and mocked.

        Args:
            settings (_type_): _description_
            command_queue (queue.Queue): _description_
            class_manager(ClassManager): A class for manage other classes
        """
        self.data_empty = {
            None: True
        }
        self.utils = class_manager.utils
        self.command_queue = command_queue

        self.word_activation = settings.word_activation
        self.split_command_exit = [settings.split_command[0],settings.split_command[1]]

    def copy_data(self,command: str):
        """Copy data from a command line.

        and return it as string or list of strings if needed for further processing in other functions.

        Args:
            command (str): Command to copy in the file
        """
        data = command
        logging.debug(f" data sended - {data}")
        self.command_queue.put(data)

    def text(self):
        """The main file for recover the command from text."""
        logging.info(" start input function")
        status = True
        while status:
            command = str(
                input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command)
            command = command.encode('ascii', 'ignore').decode('ascii')
            if self.word_activation in command:
                logging.debug(" command speech correctly ")
                self.copy_data(command)
                if any(word in command for word in self.split_command_exit):
                    status = False
            else:
                logging.warning("Remember to use the key word")
        logging.info("Shutdown in progress from input-thread")
        sys.exit()
