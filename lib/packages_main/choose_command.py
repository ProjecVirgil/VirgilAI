"""This module is mutch importante because manage all the class and procces the command."""
import queue
import string
import sys
import time
from typing import Any

import openai
from pygame import mixer
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from lib.packages_utility.logger import logging
from lib.packages_utility.sound import Audio
from lib.packages_utility.utils import Utils

from lib.packages_secondary.time import Time, diff_time
from lib.packages_secondary.change_value import VolumeMixer
from lib.packages_secondary.the_weather import Wheather
from lib.packages_secondary.calendar_rec import Calendar
from lib.packages_secondary.the_news import Newsletter
from lib.packages_secondary.searchyt import MediaPlayer
from lib.packages_secondary.manage_events import EventScheduler


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

        self.utils = Utils()
        self.audio = Audio(settings.volume, settings.elevenlabs, settings.language)

        self.volume_mixer = VolumeMixer(volume_value=100, settings=settings)
        self.time = Time(settings)
        self.wheather = Wheather(settings)
        self.event_scheduler = EventScheduler(settings)
        self.calendar = Calendar(settings)
        self.news_letter = Newsletter(settings.language, settings.synonyms_news)
        self.media_player = MediaPlayer(settings.synonyms_mediaplayer)

        model_filename = f"model/model_{self.settings.language}.pkl"
        self.loaded_model = joblib.load(model_filename)

        self.lang = settings.language
        self.result_queue = result_queue
        if self.lang == 'it':
            self.stop_words = set(stopwords.words("italian"))
        else:
            self.stop_words = set(stopwords.words("english"))

        original_punctuation = string.punctuation
        exceptions = ":'"
        self.custom_punctuation = "".join([char for char in original_punctuation if char not in exceptions])

        # Start prompt for GPT-3.5 API
        self.start_prompt = [
            {"role": "system", "content": settings.prompt}]
        self.temperature = settings.temperature
        self.max_token = settings.max_tokens
        self.api_key = settings.openai
        self.gpt_version = settings.gpt_version
        openai.api_key = self.api_key

    def off(self) -> None:
        """Function to shutdown all services and close connection with database."""
        print("\nVirgil: Shutdown in progress...", flush=True)
        data = ["spento", "spento"]
        self.result_queue.put(data)
        time.sleep(2)
        sys.exit(0)

    def get_response(self, messages: list):
        """Function for communicate whith api GPT-3.5.

        Args:
            messages (list): The contest of conversation

        Returns:
            str: The response at the message from gpt
        """
        logging.info(" I am creating the answer...")
        response = openai.chat.completions.create(
            model = self.gpt_version,
            messages = messages,
            temperature = float(self.temperature),  # 0.0 - 2.0
            max_tokens = int(self.max_token)
        )
        return response.choices[0].message


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
        logging.debug(f"Classes choised by alghorithm is {predictions}")
        try:
            if (self.settings.split_command[0] in command_worked) or (self.settings.split_command[1] in command_worked):
                self.off()
                return
            if predictions == 'OR':
                response = self.time.now()
                return response
            if self.settings.split_command[6] in command_worked or self.settings.split_command[7] in command_worked or \
                    self.settings.split_command[8] in command_worked:
                mixer.music.stop()
                return
            if predictions == 'VL':
                response = self.volume_mixer.change(command_worked)
                if response == "104":
                    print("\nVirgil: You cannot give a value less than 10, you can only give values from 100 to 10",
                        flush=True)
                    self.audio.create(file=True, namefile="ErrorValueVolume")
                    return None
                return response
            if predictions == 'MT':
                response = self.wheather.recover_weather(command_worked)
                return response
            if predictions == 'TM':
                for i in command_worked:
                    if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                        hours, minuts, calculated_hours, calculated_minuts, calculate_seconds = diff_time(i)
                        time_calculated = f"{calculated_hours} ore {calculated_minuts} minuti {calculate_seconds} secondi".split(
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
            if predictions == "GDS":
                response = self.calendar.get_date(command_worked)
                return response
            if predictions == "MC":
                for i in command_worked:
                    if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                        hours, minuts, calculated_hours, calculated_minuts, calculate_seconds = diff_time(i)
                        logging.info(
                            f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minuts)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minuts)} {self.utils.number_to_word(calculate_seconds)}")
                        return f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minuts)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.settings.phrase_time[1]} {self.utils.number_to_word(calculated_minuts)} {self.settings.phrase_time[2]} {self.utils.number_to_word(calculate_seconds)} {self.settings.phrase_time[3]}"
                result = self.calendar.diff_date(command_worked)
                return result
            if predictions == "NW":
                response = self.news_letter.create_news(command_worked)
                return response
            if predictions == "MU":
                self.media_player.play_music(command_worked)
                return
            if predictions == "EV":
                return self.event_scheduler.add_events(command_worked)
            self.start_prompt.append({"role": "user", "content": "".join(command)})
        except Exception as error:
            logging.error("Please try the command again")
            logging.error(f"ERROR: {error}")
            self.audio.create(file = True,namefile="ErrorCommand")
            return
        try:
            new_message = self.get_response(messages=self.start_prompt)
        except Exception as error:
            logging.error(
                "The OpenAI key you entered is invalid, not present, or the GPT template you selected is invalid or unavailable for your current plan. If you do not know how to obtain a valid key or select a compatible template, see the guide on GitHub for assistance and more information.")
            logging.error(error)
            self.audio.create(file=True, namefile="ErrorOpenAi")
            return
        print(f"\nVirgilio: {new_message.content}")
        self.start_prompt.append(new_message)
        return new_message.content
