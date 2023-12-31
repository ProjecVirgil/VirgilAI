"""This module is much important because manage all the class and process the command."""
import queue
import string
import sys
import time
from typing import Any

from pygame import mixer
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from lib.packages_utility.logger import logging
from lib.packages_utility.sound import Audio
from lib.packages_utility.utils import Utils

from lib.packages_secondary.time import Time, diff_time
from lib.packages_secondary.change_value import VolumeMixer
from lib.packages_secondary.the_weather import Weather
from lib.packages_secondary.calendar_rec import Calendar
from lib.packages_secondary.the_news import Newsletter
from lib.packages_secondary.searchyt import MediaPlayer
from lib.packages_secondary.manage_events import EventScheduler
from lib.packages_secondary.llm_models import LLModel


# ---- File for manage all the preset command ----



class CommandSelection:
    """This class is used to select a specific function of the assistant."""

    def __init__(self, settings,result_queue:queue.Queue) -> None:
        """Init all the settings for manage all classes.

        Args:
            settings (Settings): the dataclasses with all settings
            result_queue (Queue): The queue with results
        """
        self.settings = settings
        self.lang = settings.language

        self.utils = Utils()
        self.audio = Audio(settings.volume, settings.elevenlabs, self.lang)

        self.volume_mixer = VolumeMixer(volume_value=100, settings=settings)
        self.time = Time(self.lang,settings.split_time,settings.phrase_time)
        self.weather = Weather(settings)
        self.event_scheduler = EventScheduler(settings)
        self.calendar = Calendar(settings)
        self.news_letter = Newsletter(self.lang, settings.synonyms_news)
        self.media_player = MediaPlayer(settings.synonyms_mediaplayer)
        self.LLM = LLModel(openai_key=self.settings.openai,language=self.lang,gpt_version=settings.gpt_version,max_tokens=settings.max_tokens,prompt=settings.prompt)
        model_filename = f"model/model_{self.lang}.pkl"
        self.loaded_model = joblib.load(model_filename)

        self.result_queue = result_queue
        if self.lang == 'it':
            self.stop_words = set(stopwords.words("italian"))
        else:
            self.stop_words = set(stopwords.words("english"))

        original_punctuation = string.punctuation
        exceptions = ":'"
        self.custom_punctuation = "".join([char for char in original_punctuation if char not in exceptions])

    def off(self) -> None:
        """Function to shutdown all services and close connection with database."""
        print("\nVirgil: Shutdown in progress...", flush=True)
        data = ["shutdown", "shutdown"]
        self.result_queue.put(data)
        time.sleep(2)
        sys.exit(0)


    def clean(self, command: str, type_model: str) -> str | list[Any]:
        """Function that cleans a command.

        Args:
            command (str): the command to clean
            type_model (str): type of cleaning model(cleaning the command for
            work with the models) work (cleaning the command for work with the my code)

        Returns:
            str: The command cleaned
        """
        try:
            if type_model == 'model':
                # Convert text to lowercase
                command = command.lower()
                # Remove punctuation
                command = command.translate(str.maketrans(' ', ' ', self.custom_punctuation))
                # Remove stopwords and lemmatize the words
                words = command.split()
                return ' '.join(words)
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
        predictions = self.loaded_model.predict([self.clean(command, "model")])
        command_worked = self.clean(command, "work")
        logging.debug(f"Classes chosen by algorithm is {predictions}")
        try:
            if (self.settings.split_command[0] in command_worked) or (self.settings.split_command[1] in command_worked):
                self.off()
                return
            elif predictions == 'OR':
                response = self.time.now()
                return response
            elif self.settings.split_command[6] in command_worked or self.settings.split_command[7] in command_worked or \
                    self.settings.split_command[8] in command_worked:
                mixer.music.stop()
                return
            elif predictions == 'VL':
                response = self.volume_mixer.change(command_worked)
                if response == "104":
                    print("\nVirgil: You cannot give a value less than 10, you can only give values from 100 to 10",
                        flush=True)
                    self.audio.create(file=True, namefile="ErrorValueVolume")
                    return None
                return response
            elif predictions == 'MT':
                response = self.weather.recover_weather(command_worked)
                return response
            elif predictions == 'TM':
                for i in command_worked:
                    if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                        hours, minutes, calculated_hours, calculated_minutes, calculate_seconds = diff_time(i)
                        time_calculated = f"{calculated_hours} hours {calculated_minutes} minutes {calculate_seconds} seconds".split(
                            " ")
                        my_time = self.time.conversion(list(time_calculated))
                        return str(my_time)
                try:
                    my_time = self.time.conversion(command_worked)
                    return str(my_time)
                except IndexError:
                    logging.error("Please try the command again")
                    self.audio.create(file=True, namefile="GenericError")
                    return
            elif predictions == "GDS":
                response = self.calendar.get_date(command_worked)
                return response
            elif predictions == "MC":
                for i in command_worked:
                    if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                        hours, minutes, calculated_hours, calculated_minutes, calculate_seconds = diff_time(i)
                        logging.info(
                            f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minutes)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minutes)} {self.utils.number_to_word(calculate_seconds)}")
                        return f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minutes)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.settings.phrase_time[1]} {self.utils.number_to_word(calculated_minutes)} {self.settings.phrase_time[2]} {self.utils.number_to_word(calculate_seconds)} {self.settings.phrase_time[3]}"
                result = self.calendar.diff_date(command_worked)
                return result
            elif predictions == "NW":
                response = self.news_letter.create_news(command_worked)
                return response
            elif predictions == "MU":
                self.media_player.play_music(command_worked)
                return
            elif predictions == "EV":
                return self.event_scheduler.add_events(command_worked)
            else:
                result = self.LLM.gen_response("".join(command))
                logging.info(f"Generated response: {result}")
                return result
        except Exception as error: # If an error appears
                    logging.error("Please try the command again")
                    logging.error(f"ERROR: {error}")
                    self.audio.create(file = True,namefile="ErrorCommand")
                    return
