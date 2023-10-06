"""The input file for the voice with mic."""
import json
import unicodedata

import speech_recognition as sr

from lib.packages_utility.logger import logging
from lib.packages_utility.utils import Utils


# ----- File to take the input by the microphone -----
def copy_data(command: str) -> None:
    """Copy data from one command to another.

    Args:
        command (str): The actual command
    """
    data = {
        command: False
    }
    logging.debug(f" data sended - {data}")
    with open("connect/command.json", 'w', encoding="utf8") as comandi:
        json.dump(data, comandi, indent=4)


class VocalInput:
    """Class that takes voice inputs from a user and returns them in text format."""

    def __init__(self, settings) -> None:
        """Init func for some settings.

        Args:
            settings (Settings): settings dataclasses
        """
        self.data_empty = {
            None: True
        }
        self.utils = Utils()
        self.listener = sr.Recognizer()

        # init the recognizer
        self.listener.operation_timeout = int(settings.operation_timeout)
        self.listener.dynamic_energy_threshold = bool(settings.dynamic_energy_threshold)
        self.listener.energy_threshold = int(settings.energy_threshold)
        self.word_activation = settings.word_activation

    def listening(self):
        """Listens for commands using Google Speech Recognition API.It will return the recognized words or phrases."""
        command = ""
        logging.debug(" start input function")
        self.utils.clean_buffer(data_empty=self.data_empty, file_name="command")
        status = True
        while status:
            try:
                with sr.Microphone() as source:
                    logging.debug(" I'm hearing...")
                    voice = self.listener.listen(source, 5, 15)
                    command = self.listener.recognize_google(voice, language='it-it')
                    command = command.lower()
                    command = unicodedata.normalize('NFKD', command)
                    command = command.encode('ascii', 'ignore').decode('ascii')
                    logging.debug(f" command rude acquired: {command} ")
                    if self.word_activation in command:
                        copy_data(command)
                        if "spegniti" in command:
                            status = False
            except sr.exceptions.WaitTimeoutError:
                try:
                    if "spegniti" in command:
                        status = False
                    else:
                        logging.warning(" Microphone unmuted or something went wrong")
                except UnboundLocalError:
                    pass
