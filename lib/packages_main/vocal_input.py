""""""
import json
import unicodedata

import speech_recognition as sr

from lib.packages_utility.logger import Logger
from lib.packages_utility.utils import Utils

# ----- File to take the input by the microphone -----
class VocalInput:
    """
    Class that takes voice inputs from a user and returns them in text format
    """
    def __init__(self,settings) -> None:
        self.data_empty = {
            None:True
            }
        self.logger = Logger()
        self.utils = Utils()
        self.listener = sr.Recognizer()

        # init the recognizer
        self.listener.operation_timeout = int(settings.operation_timeout)
        self.listener.dynamic_energy_threshold = bool(settings.dynamic_energy_threshold)
        self.listener.energy_threshold = int(settings.energy_threshold)
        self.word_activation = settings.word_activation

    def copy_data(self,command:str) -> None:
        """
        Copy data from one command to another

        Args:
            command (str): The actual command
        """
        data = {
            command:False
            }
        print(self.logger.log(f" data sended - {data}"), flush=True)
        with open("connect/command.json", 'w',encoding="utf8") as comandi:
            json.dump(data, comandi,indent=4)

    def listening(self):
        """
        Listens for commands using Google Speech Recognition API.It will return the recognized words or phrases.
        """
        command = ""
        print(self.logger.log(" start input function"), flush=True)
        self.utils.clean_buffer(data_empty=self.data_empty,file_name="command")
        status  = True
        while status:
            try:
                with sr.Microphone() as source:
                    print(self.logger.log(" I'm hearing..."), flush=True)
                    voice = self.listener.listen(source,5,15)
                    command = self.listener.recognize_google(voice,language='it-it')
                    command = command.lower()
                    command = unicodedata.normalize('NFKD', command)
                    command = command.encode('ascii', 'ignore').decode('ascii')
                    print(self.logger.log(f" command rude acquired: {command} "), flush=True)
                    if self.word_activation in command:
                        self.copy_data(command)
                        if "spegniti" in command:
                            status = False
            except sr.exceptions.WaitTimeoutError:
                try:
                    if "spegniti" in command:
                        status = False
                    else:
                        print(self.logger.log(" Microphone unmuted or something went wrong"),
                              flush=True)
                except UnboundLocalError:
                    pass
