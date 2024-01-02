"""The process file for the command."""
import queue
import threading

from colorama import Fore
import nltk

from lib.packages_main.command_processor import CommandProcessor
from lib.packages_utility.db_manager import DBManagerSettings
from lib.packages_utility.logger import logging


# ----- File to elaborate the input  -----

class Process:
    """This class is responsible for processing the user's command and returning a response from Virgil API and other APIs."""

    def __init__(self, settings,command_queue:queue.Queue,result_queue:queue.Queue,class_manager) -> None:
        """The process class.

        Args:
            settings (_type_): _description_
            command_queue (queue.Queue): _description_
            result_queue (queue.Queue): _description_
            class_manager(_type_): _description_
        """
        self.data_empty = {
            "0": [None, None, True]
        }
        nltk.download('punkt')
        nltk.download('stopwords')

        self.utils = class_manager.utils
        self.command_queue = command_queue
        self.result_queue = result_queue
        self.command_processor = CommandProcessor(settings,result_queue,class_manager)
        self.word_activation = settings.word_activation
        self.split_command_exit = [settings.split_command[0],settings.split_command[1]]

    def clean_command(self, command: str) -> str:
        """Delete the word activation and strip from the command.

        Args:
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            command = str(command).split(f"{self.word_activation} ")[1].strip()
            logging.debug(f" command processed: {command} ")
            return command
        except IndexError:
            # If command contain only virgil word
            logging.debug(f" command processed: {command} ")
            return command.strip()

    def send(self, command) -> None:
        """Send the command in the process file (choose_command.py) for the elaboration.

        Args:
            command (str): the command to send
        """
        command = self.clean_command(command)
        result = self.command_processor.send_command(command)
        self.result_queue.put([command, result])

    class EventThread(threading.Thread):
        """Class that manage the event of a thread.

        Args:
            threading (Thread)
        """

        def __init__(self, logger):
            """Init the class.

            Args:
                logger (logger): The class for print the log (temporary)
            """
            threading.Thread.__init__(self)
            self.daemon = True
            self.logger = logger


        def check_event(self) -> None:
            """Check if there is an event."""
            db_manager = DBManagerSettings()
            logging.debug("update the reminder")
            db_manager.set_reminder(value=0)

        def run(self) -> None:
            """Run the function."""
            self.check_event()

    def main(self) -> None:
        """Main method of the program."""
        logging.info(Fore.GREEN + " THE ASSISTANT IS ONLINE  " + Fore.BLUE)
        thread = self.EventThread(logging)
        thread.start()
        status = True
        while status:
            command = self.command_queue.get()
            if any(word in command for word in self.split_command_exit):
                command = f"virgilio {self.split_command_exit[1]}"
                logging.info("Shutdown in progress from process thread")
                status = False
            if command:
                logging.debug(f" command processed: {command}")
                self.send(command)


