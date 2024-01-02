"""This module is much important because manage all the class and process the command."""
import queue
import sys
import time

from pygame import mixer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from lib.packages_utility.logger import logging
from lib.packages_utility.command_selector import CommandSelector
from lib.packages_utility.request import MakeRequests

# ---- File for manage all the preset command ----



class CommandProcessor:
    """This class is used to select a specific function of the assistant."""

    def __init__(self, settings,result_queue:queue.Queue,class_manager) -> None:
        """Init all the settings for manage all classes.

        Args:
            settings (Settings): the dataclasses with all settings
            result_queue (Queue): The queue with results
            class_manager (ClassManager): This dataclasses manage some classes like utils and audio
        """
        self.settings = settings
        self.audio = class_manager.audio

        self.command_selector  = CommandSelector(settings,class_manager)
        self.request_maker = MakeRequests(settings.language)

        if settings.language == 'it':
            self.stop_words = set(stopwords.words("italian"))
        else:
            self.stop_words = set(stopwords.words("english"))

        self.result_queue = result_queue

    def off(self) -> None:
        """Function to shutdown all services and close connection with database."""
        print("\nVirgil: Shutdown in progress...", flush=True)
        data = ["shutdown", "shutdown"]
        self.result_queue.put(data)
        time.sleep(2)
        sys.exit(0)

    def clean(self, command: str, type_model: str) -> str | list[str]:
        """Function that cleans a command.

        Args:
            command (str): the command to clean
            type_model (str): type of cleaning model(cleaning the command for
            work with the models) work (cleaning the command for work with the my code)

        Returns:
            str: The command cleaned
        """
        try:
            if type_model == 'work':
                filtered_tokens = []
                tokens = word_tokenize(command.lower().strip())
                for word in tokens:
                    if word not in (",", "?") and word not in self.stop_words:
                        filtered_tokens.append(word)
                logging.debug(f" command processed: {filtered_tokens} ")
                return filtered_tokens
        except IndexError:
            return command

    def send_command(self, command:str) -> str | None:  # noqa: PLR0911, PLR0912, PLR0915
        """Function to process a command received by user and send on process.

        Args:
            command (str): command cleaned

        Returns:
            str: The response at the command
        """
        mixer.init()
        command_worked = self.clean(command, "work")
        predict = self.request_maker.get_category(command)
        logging.info(f"Classes chosen by algorithm is {predict}")

        table_function = {
            'OR': self.command_selector.get_time,
            'VL': self.command_selector.change_volume,
            'MT': self.command_selector.get_weather,
            'TM': self.command_selector.get_timer,
            'GDS':self.command_selector.get_date,
            'MC': self.command_selector.get_mc,
            'NW': self.command_selector.get_news,
            'MU': self.command_selector.play_music,
            'EV': self.command_selector.add_events,
            'AL': self.command_selector.generate_response
        }

        try:
            # * --- SPECIAL COMMAND -----
            if (self.settings.split_command[0] in command_worked) or (self.settings.split_command[1] in command_worked):
                self.off()
                return
            elif (self.settings.split_command[6] in command_worked) or (self.settings.split_command[7] in command_worked) or (self.settings.split_command[8] in command_worked):
                mixer.music.stop()
                return

            # * --- STANDARD COMMAND -----
            elif(predict != 'AL'):
                logging.info("Command understood correctly")
                return table_function[predict](command_worked)
            else:
                logging.info("Let me think I am generating the answer...")
                return table_function[predict](command)
        except Exception as error: # If an error appears
                    logging.error("Please try the command again")
                    logging.error(f"ERROR: {error}")
                    self.audio.create(file = True,namefile="ErrorCommand")
                    return
