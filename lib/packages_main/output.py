"""Class for manage the output of command."""
import queue
import time
import threading
import sys

from colorama import Style, Fore
import pyfiglet
from pygame import mixer

from lib.packages_utility.logger import logging
from lib.packages_utility.db_manager import DBManagerSettings




class Output:
    """Output class for the bot to output messages and errors on console or file."""

    def __init__(self, settings,result_queue:queue.Queue,class_manager) -> None:
        """Init all classes for the Output function.

        Args:
            settings (Settings): settings dataclasses with all settings
            result_queue (Queue): The queue with results
            class_manager(ClassManager): A class for manage other classes
        """
        mixer.init()
        self.class_manager = class_manager
        self.settings = settings
        self.utils = self.class_manager.utils
        self.event_scheduler = self.class_manager.event_scheduler
        self.audio = self.class_manager.audio
        self.result_queue = result_queue

        self.lang = settings.language
        self.split_command_exit = [settings.split_command[0],settings.split_command[1]]


    def check_reminder(self) -> bool:
        """Check if there is any reminder set up by user. If so it will send him a message.

        Returns:
            bool: Reminder send?
        """
        logging.info("Check your commitments")
        self.db_manager = DBManagerSettings()
        if self.db_manager.get_reminder() == 0:
            self.db_manager.set_reminder(value=1)
            return False
        return True

    class TimerThread(threading.Thread):
        """Timer thread class to run the timer function and stop when needed.

        Args:
            threading (_type_): _description_
        """

        def __init__(self, interval, command, settings,audio):
            """Init file for the class of Thread.

            Args:
                interval (int): The duration of time.sleep
                command (_type_): The command
                settings(Settings): All the settings
                audio(Audio): An audio instance
            """
            threading.Thread.__init__(self)
            self.interval = interval
            self.daemon = True
            self.command = command
            self.settings = settings
            self.audio = audio

        def timer(self, my_time: int, command: str) -> None:
            """Timer function.

            Args:
                my_time (int): The time in second
                command (_type_): The command
            """
            if self.settings.phrase_output[0] in command:
                time.sleep(my_time)
            else:
                time.sleep(my_time)
                self.audio.create(file=True, namefile="timerEndVirgil")

        def run(self) -> None:
            """Function tu run the timer."""
            self.timer(self.interval,self.command)

    def shutdown(self) -> None:
        """Function to shut down the programm."""
        logging.info("Shutdown in progress from output-thread")
        self.audio.create(file=True, namefile="FinishVirgil")
        print(Style.BRIGHT + Fore.MAGENTA + pyfiglet.figlet_format("Thanks for using Virgil",
                                                                   font="digital",
                                                                   justify="center",
                                                                   width=110),
              flush=True)
        print(Fore.LIGHTMAGENTA_EX + " - credit: @retr0", flush=True)
        time.sleep(2)
        sys.exit(0)

    def out(self):  # noqa: PLR0912
        """Main function."""
        self.audio.create(file=True, namefile="EntryVirgil")
        time.sleep(5)
        while True:
                data = self.result_queue.get()
                command,result  = data[0], data[1]
                if result:
                    if "shutdown" in command:
                        self.shutdown()
                    if "volume" in command:
                        mixer.music.set_volume(float(result))
                        mixer.music.unload()
                        mixer.music.load('assets/audio/bipEffectCheckSound.mp3')
                        mixer.music.play()
                        logging.info(f"Volume changed correctly to {int(result) * 100}% ")
                    elif "timer" in command or self.settings.split_output[0] in command:
                        logging.debug(f"The timer is started see you in {result} second"),
                        if "timer" in command:
                            if self.lang != "en":
                                self.audio.create(
                                    f"{self.settings.phrase_output[0]} {self.utils.number_to_word(result)} {self.settings.phrase_output[1]}")
                            else:
                                self.audio.create(
                                    f"{self.settings.phrase_output[0]} {result} {self.settings.phrase_output[1]}")
                        else:
                            self.audio.create(file=True, namefile="ClockImposter")
                        thread = self.TimerThread(int(result), command,self.settings,self.class_manager.audio)
                        thread.start()
                    else:
                        self.audio.create(result)
                        logging.debug(result)


                    if not self.check_reminder():
                        logging.info("Send notify for today event")
                        result = self.event_scheduler.send_notify()
                        time.sleep(10)
                        self.audio.create(result)


