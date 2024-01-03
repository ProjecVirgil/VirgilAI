"""This file manage all the time function.

like:

- The time
- Timer
- Clock
- more

"""
import datetime
import time

from lib.packages_utility.logger import logging


# ---- This file get the current time and more ----

def diff_time(index_time: str) -> tuple:
    """This function will take an index time and compare it with the actual time.

    Args:
        index_time (str): the index of the time in the sentence

    Returns:
        tuple: The complete date about the time and
        the difference with the current time
    """
    current_time = datetime.datetime.now().time()
    try:
        query_splitted = index_time.split(":")
        hours = query_splitted[0]
        minutes = query_splitted[1]
    except ValueError:
        query_splitted = index_time.split(" e ")
        hours = query_splitted[0]
        minutes = query_splitted[1]

    time_string = f"{hours}:{minutes}"

    time_formatted = datetime.datetime.strptime(time_string, "%H:%M").time()

    current_date = datetime.datetime.combine(datetime.date.today(), current_time)
    specify_date = datetime.datetime.combine(datetime.date.today(), time_formatted)

    diff_time = specify_date - current_date

    calculated_hours, rest = divmod(diff_time.seconds, 3600)
    calculated_minutes, calculate_seconds = divmod(rest, 60)

    return hours, minutes, calculated_hours, calculated_minutes, calculate_seconds


class Time:
    """This class is used to return a various things like the Actual time, the time difference and more."""

    def __init__(self, language,split_time,phrase_time,utils):
        """Constructor for the class Time.

        Args:
            language (str): The language
            split_time (list): A list of word from settings
            phrase_time (list): A list of word from settings
            utils (Utils): A utils instance
        """
        self.utils = utils

        self.lang = language
        self.split_time = split_time
        self.phrase_time = phrase_time

    def now(self) -> str:
        """Return the current  time.

        Returns:
            str: The current time
        """
        time_tuple = time.localtime()  # get struct_time
        hours = time.strftime('%H', time_tuple)
        minutes = time.strftime('%M', time_tuple)
        if self.lang != "en":
            hours = self.utils.number_to_word(hours)
            minutes = self.utils.number_to_word(minutes)
        time_string = f"{self.phrase_time[4]} {str(hours)} {self.split_time[3]} {str(minutes)}  {self.split_time[11]}"
        logging.info(time.strftime("\nVirgil: They are the %H and %M minutes", time_tuple))
        return time_string

    def conversion(self, command) -> int:  # noqa: PLR0911
        """This function try to take the timer time and convert everything to seconds.

        Args:
            command (str): The input sentence

        Returns:
            int: The time in second
        """
        hashmap = {
            "s": None,
            "m": None,
            "h": None,
        }

        for index, _ in enumerate(command):
            if command[index].isdigit():
                if command[index + 1] in (self.split_time[9], self.split_time[10]):
                    hashmap["h"] = command[index]
                elif command[index + 1] in (self.split_time[11], self.split_time[12]):
                    hashmap["m"] = command[index]
                elif command[index + 1] in (self.split_time[13], self.split_time[14]):
                    hashmap["s"] = command[index]

        if (hashmap["h"] is not None) and (hashmap["m"] is not None) and (hashmap["s"] is not None):
            hours = int(hashmap["h"])
            minutes = int(hashmap["m"])
            seconds = int(hashmap["s"])
            sum_seconds = hours * 3600 + minutes * 60 + seconds
            return sum_seconds

        if (hashmap["h"] is not None) and (hashmap["m"] is not None):
            hours = int(hashmap["h"])
            minutes = int(hashmap["m"])
            sum_seconds = hours * 3600 + minutes * 60
            return sum_seconds

        if (hashmap["m"] is not None) and (hashmap["s"] is not None):
            minutes = int(hashmap["m"])
            seconds = int(hashmap["s"])
            sum_seconds = minutes * 60 + seconds
            return sum_seconds

        if (hashmap["h"] is not None) and (hashmap["s"] is not None):
            hours = int(hashmap["h"])
            seconds = int(hashmap["s"])
            sum_seconds = hours * 3600 + seconds
            return sum_seconds

        if hashmap["h"] is not None:
            return int(hashmap["h"]) * 3600
        if hashmap["m"] is not None:
            return int(hashmap["m"]) * 60

        return int(hashmap["s"])
