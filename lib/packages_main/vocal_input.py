"""The input file for the voice with mic."""
import queue
import unicodedata

import speech_recognition as sr

from lib.packages_utility.logger import logging

# ----- File to take the input by the microphone -----


class VocalInput:
    """Class that takes voice inputs from a user and returns them in text format."""

    def __init__(self, settings,command_queue:queue.Queue,class_manager) -> None:
        """Init func for some settings.

        Args:
            settings (Settings): settings dataclasses
            command_queue:(Queue): The command queue for thread
        """
        self.data_empty = {
            None: True
        }
        self.utils = class_manager.utils
        self.listener = sr.Recognizer()
        self.command_queue = command_queue

        # init the recognizer
        self.listener.operation_timeout = int(settings.operation_timeout)
        self.listener.dynamic_energy_threshold = bool(settings.dynamic_energy_threshold)
        self.listener.energy_threshold = int(settings.energy_threshold)
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

    def listening(self):
        """Listens for commands using Google Speech Recognition API.It will return the recognized words or phrases."""
        command = ""
        logging.debug(" start input function")
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
                        self.copy_data(command)
                        if any(word in command for word in self.split_command_exit):
                            status = False
            except sr.exceptions.WaitTimeoutError:
                try:
                    if any(word in command for word in self.split_command_exit):
                        status = False
                    else:
                        logging.warning(" Microphone unmuted or something went wrong")
                except UnboundLocalError:
                    pass
