"""
_summary_

"""
import json
import unicodedata

import speech_recognition as sr

from lib.logger import Logger
from lib.utils import Utils


# ----- File to take the input by the microphone -----
class VocalInput:
    """_summary_
    """
    def __init__(self) -> None:
        self.data_empty = {
            None:True
            }
        self.logger = Logger()
        self.utils = Utils()
        self.listener = sr.Recognizer()
        with open('setup/settings.json',encoding="utf8") as file:
            settings = json.load(file)
            # init the recognizer
            self.listener.operation_timeout = int(settings['operation_timeout'])
            self.listener.dynamic_energy_threshold = bool(settings['dynamic_energy_threshold'])
            self.listener.energy_threshold = int(settings['energy_threshold'])
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
    #Main
    def speech(self):
        """_summary_
        """
        command = ""
        print(self.logger.log(" start hearing function"), flush=True)
        self.utils.clean_buffer(data_empty=self.data_empty,file_name="command")
        status  = True
        while status:
            try:
                with sr.Microphone() as source:
                    print(self.logger.log(" I'm hearing..."), flush=True)
                    voice = self.listener.listen(source,5,15)
                    command = self.listener.recognize_google(voice,language='it-it')
                    print(self.logger.log(" command acquired"), flush=True)
                    command = command.lower()
                    command = unicodedata.normalize('NFKD', command)
                    command = command.encode('ascii', 'ignore').decode('ascii')
                    print(self.logger.log(f" command rude acquired: {command} "), flush=True)
                    if self.word_activation in command:
                        print(self.logger.log(" command speech correctly "), flush=True)
                        self.copy_data(command)
                        if "spegniti" in command:
                            print(self.logger.log(" shutdown in progress..."), flush=True)
                            status = False
            except sr.exceptions.WaitTimeoutError:
                try:
                    if "spegniti" in command:
                        print(self.logger.log(" shutdown in progress"), flush=True)
                        status = False
                    else:
                        print(self.logger.log(" Microphone unmuted or something went wrong"),
                              flush=True)
                except UnboundLocalError:
                    pass
                