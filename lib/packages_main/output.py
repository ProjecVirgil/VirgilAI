"""Class for manage the output of command."""
import json
import time
import threading
import sys

from colorama import Style, Fore
import pyfiglet
from pygame import mixer

from lib.packages_utility.sound import Audio
from lib.packages_utility.logger import logging
from lib.packages_utility.utils import Utils

from lib.packages_secondary.manage_events import EventScheduler


def update_json_value(key: int, new_value: bool) -> None:
    """Update a value in settings JSON file with given key name.

    Args:
        key (str): Command to change value
        new_value (bool): True/False
    """
    # Apri il file JSON e carica i dati
    with open("connect/res.json", encoding="utf8") as file:
        data = json.load(file)

    # Modifica il valore desiderato
    data["0"][key] = new_value

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("connect/res.json", 'w', encoding="utf8") as file:
        json.dump(data, file, indent=4)


def check_reminder() -> bool:
    """Check if there is any reminder setted up by user. If so it will send him a message.

    Returns:
        bool: Rimender send?
    """
    with open("connect/reminder.txt", encoding="utf8") as file:
        if file.read() == "0":
            with open("connect/reminder.txt", "w", encoding="utf8") as file_to_write:
                file_to_write.write("1")
            return False
        return True


def recover_data() -> tuple:
    """Function to recover data from a previous session.

    Returns:
        tuple: The data recovered.
    """
    with open("connect/res.json", encoding="utf8") as file:
        data = json.load(file)
        res = data["0"][1]
        command = data["0"][0]
        is_used = data["0"][2]
        return res, command, is_used


class Output:
    """Output class for the bot to output messages and errors on console or file."""

    def __init__(self, settings) -> None:
        """Init all classes for the Output function.

        Args:
            settings (Settings): settings dataclasses with all settings
        """
        mixer.init()

        self.settings = settings

        self.utils = Utils()
        self.event_scheduler = EventScheduler(settings)
        self.audio = Audio(settings.volume, settings.elevenlabs, settings.language)

        self.lang = settings.language
        self.split_command = settings.split_command

    def timer(self, my_time: int, command: str) -> None:
        """Timer function that runs every 3 seconds.

        Args:
            my_time (int): The time in second
            command (_type_): The command
        """
        if self.settings.phrase_outputs[0] in command:
            time.sleep(my_time)
        else:
            time.sleep(my_time)
            self.audio.create(file=True, namefile="timerEndVirgil")

    class TimerThread(threading.Thread):
        """Timer thread class to run the timer function and stop when needed.

        Args:
            threading (_type_): _description_
        """

        def __init__(self, interval, command):
            """Init file for the class of Thread.

            Args:
                interval (int): the duration of time.sleep
                command (_type_): the command
            """
            threading.Thread.__init__(self)
            self.interval = interval
            self.daemon = True
            self.command = command

        def run(self) -> None:
            """Function tu run the timer."""
            output_instance = Output(settings=self.settings)
            output_instance.timer(self.interval, self.command)

    def shutdown(self) -> None:
        """Function to shut down the programm."""
        logging.info(" shutdown in progress...")
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
            try:
                result, command, is_used = recover_data()
                if result is not None and is_used is False:
                    if any(word in result for word in self.split_command):
                        self.shutdown()
                    if "volume" in command:
                        mixer.music.set_volume(float(result))
                        mixer.music.unload()
                        mixer.music.load('asset/bipEffectCheckSound.mp3')
                        mixer.music.play()
                        logging.info(f" volume changed correctly to {result * 100}% ")
                    elif "timer" in command or self.settings.split_output[0] in command:
                        logging.debug(f" the timer is started see you in {result} second"),
                        if "timer" in command:
                            if self.lang != "en":
                                self.audio.create(
                                    f"{self.settings.phrase_output[0]} {self.utils.number_to_word(result)} {self.settings.phrase_output[1]}")
                            else:
                                self.audio.create(
                                    f"{self.settings.phrase_output[0]} {result} {self.settings.phrase_output[1]}")
                        else:
                            self.audio.create(file=True, namefile="ClockImposter")
                        thread = self.TimerThread(int(result), command)
                        thread.start()
                    else:
                        self.audio.create(result)
                        logging.debug(result)
                    update_json_value(2, True)

                    if not check_reminder():
                        logging.info(" send notify for today event")
                        result = self.event_scheduler.send_notify()
                        time.sleep(10)
                        self.audio.create(result)
                else:
                    pass
            except json.decoder.JSONDecodeError:
                logging.debug("Nothing was found in the json")
