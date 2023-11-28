"""The procces file for the command."""
import queue
import threading

from colorama import Fore
import nltk

from lib.packages_utility.logger import logging
from lib.packages_utility.request import MakeRequests
from lib.packages_utility.utils import Utils
from lib.packages_main.choose_command import CommandSelection


# ----- File to elaborate the input  -----


def check_event() -> None:
    """Check if there is an event."""
    logging.debug("update the reminder")
    with open("connect/reminder.txt", "w", encoding="utf8") as file:
        file.write("0")


class Process:
    """This class is responsible for processing the user's command and returning a response from Virgil API and other APIs."""

    def __init__(self, settings,command_queue:queue.Queue,result_queue:queue.Queue) -> None:
        """The process class.

        Args:
            settings (_type_): _description_
            command_queue (queue.Queue): _description_
            result_queue (queue.Queue): _description_
        """
        self.data_empty = {
            "0": [None, None, True]
        }
        nltk.download('punkt')
        nltk.download('stopwords')

        self.request_maker = MakeRequests()
        self.utils = Utils()
        self.command_queue = command_queue
        self.result_queue = result_queue

        self.command_selection = CommandSelection(settings,result_queue)

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
            return command

    def send(self, command) -> None:
        """Send the command in the process file (choose_command.py) for the elaboration.

        Args:
            command (str): the command to send
        """
        command = self.clean_command(command)
        result = self.command_selection.send_command(command)
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

        def run(self) -> None:
            """Run the function."""
            check_event()

    def main(self) -> None:
        """Main method of the program."""
        logging.info(Fore.GREEN + " THE ASSISTENT IS ONLINE  " + Fore.BLUE)
        thread = self.EventThread(logging)
        thread.start()
        status = True
        while status:
            command = self.command_queue.get()
            if any(word in command for word in self.split_command_exit):
                command = f"virgilio {self.split_command_exit[1]}"
                logging.info("Shutdown in progress from procces thread")
                status = False
            if command:
                logging.debug(f" command processed: {command}")
                self.send(command)
            else:
                pass

