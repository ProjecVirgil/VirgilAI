"""A module for manage all thread.

Returns:
        _type_: _description_
"""
import threading
import queue
from dataclasses import dataclass

from lib.packages_utility.logger import logging

from colorama import Fore,Style
from lib.packages_main.output import Output
from lib.packages_main.text_input import TextInput
from lib.packages_main.vocal_input import VocalInput
from lib.packages_main.process import Process

from lib.packages_utility.sound import Audio
from lib.packages_utility.utils import Utils
from lib.packages_utility.db_manager import DBManagerSettings
from lib.packages_secondary.manage_events import EventScheduler
from lib.packages_secondary.calendar_rec import Calendar

def choice_input():
    """This function is used when you want to choose between the text input or Voice input.

    Returns:
        str: the type of input
    """
    while True:
        text_or_speech = str(input(
            Fore.GREEN + Style.BRIGHT + "You want a text interface (T) or recognize interface(R) T/R: " + Style.RESET_ALL)).upper()
        if text_or_speech == 'T':
            return 1
        elif text_or_speech == 'R':
            return 0
        else:
            logging.warning(" Select a valid choice please")

@dataclass(slots=True, frozen=True)
class ClassManager:
    """This class manage classes instances and methods.

    Only for some classes
    """
    audio:Audio
    utils:Utils
    db_manager_settings:DBManagerSettings
    event_scheduler:EventScheduler
    calendar:Calendar

class ThreadManager:
    """This class manages all threads and processes that are running in the background."""
    def __init__(self,settings,default_start:str):
        """Init function.

        Args:
            settings (_type_): _description_
            default_start (str): _description_
        """
        self.settings = settings
        self.default_start = default_start

        self.command = queue.Queue()
        self.result = queue.Queue()

        self.threads = []

        self.class_manager = ClassManager(
            Audio(settings.volume, settings.elevenlabs, settings.language),
            Utils(),
            DBManagerSettings(),
            EventScheduler(self.settings),
            Calendar(self.settings),
        )

    def init(self):
        """This method initialize all threads."""
        output = Output(self.settings,self.result,self.class_manager)
        process = Process(self.settings,self.command,self.result,self.class_manager)
        if self.default_start == 'N':
            text_or_speech = choice_input()
            if text_or_speech == 1:
                text_input = TextInput(self.settings,self.command,self.class_manager)
                self.threads.append(threading.Thread(target=text_input.text))
                self.threads.append(threading.Thread(target=process.main))
                self.threads.append(threading.Thread(target=output.out))
            elif text_or_speech == 0:
                vocal_input = VocalInput(self.settings,self.command,self.class_manager)
                self.threads.append(threading.Thread(target=vocal_input.listening))
                self.threads.append(threading.Thread(target=process.main))
                self.threads.append(threading.Thread(target=output.out))
            else:
                logging.warning(" Select a valid choice please")
        elif self.default_start == 'T':
            text_input = TextInput(self.settings,self.command,self.class_manager)
            self.threads.append(threading.Thread(target=text_input.text))
            self.threads.append(threading.Thread(target=process.main))
            self.threads.append(threading.Thread(target=output.out))
        else:
            vocal_input = VocalInput(self.settings,self.command,self.class_manager)
            self.threads.append(threading.Thread(target=vocal_input.listening))
            self.threads.append(threading.Thread(target=process.main))
            self.threads.append(threading.Thread(target=output.out))

    def start(self):
        """This method is used to start the thread of the application."""
        for i,thread in enumerate(self.threads):
            logging.info(f"Start thread number: {i}")
            thread.start()
