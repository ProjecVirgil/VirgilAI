"""This file manage the call at the API for the weather."""
import calendar
import datetime

import csv
import requests

from lib.packages_utility.logger import logging


# ---- This file get the Meteo of all week ----


def get_current_week_days() -> list:
    """This function returns a current week.

    Returns:
        list: the week days
    """
    today = datetime.date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    week_days = [min(today.day + i, days_in_month) for i in range(7)]
    repetitions = 0
    for i in week_days:
        if i == 31:  # noqa: PLR2004
            repetitions += 1
            if repetitions >= 2:  # noqa: PLR2004
                week_days[7 - repetitions + 1] = repetitions - 1
    return week_days


def is_valid_date(days, command):
    """This function checks that the date given by user.

    Is valid or not and it also check that the day of the month is correct.

    Args:
        days (_type_): A list of day in the months
        command (_type_): The input command

    Returns:
        bool: Valid/Not Valid
    """
    return any(str(i) in command for i in days)


class Weather:
    """This class manage to get the weather for a specific day and time."""

    def __init__(self, settings,audio,utils) -> None:
        """Init file for the weather manage.

        Args:
            settings (Settings): The dataclasses with all the settings
            audio (Audio): Audio instance
            utils (Utils): Utils instance
        """
        self.audio = audio
        self.utils = utils

        self.city = settings.city
        self.lang = settings.language
        self.split_weather = settings.split_weather
        self.phrase_weather = settings.phrase_weather
        self.wwc_weather = settings.wwc_weather

    # Init the api weather
    def get_url(self, city) -> str:
        """This function init the url with the parameters to call the API weather.

        Args:
            city (_type_): The city from which the url is obtained

        Returns:
            url: The final url generated
        """
        url = ""
        latitude, longitude = self.utils.get_coordinates(city)
        if latitude is not None and longitude is not None:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FLondon"
        return url

    def recover_city(self, command: list) -> str:
        """This method will be used to recover the city name from sentence.

        Args:
            command (str): sentence

        Returns:
            str: City choose if the city not specify
        """
        minimum_accuracy = 3
        result_list = []
        min_distance = 100000000
        with open("assets/worldcities.csv", encoding='utf-8') as csvfile:
            for word in command:
                city = ""
                latitude, longitude = self.utils.get_coordinates(word)
                if latitude is not None and longitude is not None:
                        csvreader = csv.reader(csvfile, delimiter=';')
                        for row in csvreader:
                            if row[0] == "city":
                                continue
                            if row[0].lower() == city:
                                return city
                            result = self.utils.haversine_distance((latitude, longitude), (float(row[2]), float(row[3])))
                            if result < min_distance:
                                min_distance = result
                                city = row[1]
                        result_list.append((city, min_distance))
            result_list = sorted(result_list, key=lambda x: x[1])

        if result_list[0][1] < minimum_accuracy:
            city_correct = result_list[0][0]
            logging.debug(f" City in the phrase chosen: {city_correct}")
            return city_correct
        logging.debug(" Default city choose")
        return self.city

    def recover_day(self, command: str) -> tuple:  # noqa: PLR0911
        """This function recovers the day from the user input.

        Args:
            command (str): sentence

        Returns:
            tuple: Index of day and the day
        """
        days = get_current_week_days()
        if self.split_weather[1] in command or str(days[0]) in command:
            return 0, days[0]
        if self.split_weather[2] in command or str(days[1]) in command:
            return 1, days[1]
        if self.split_weather[3] in command or str(days[2]) in command:
            return 2, days[2]
        if str(days[3]) in command:
            return 3, days[3]
        if str(days[4]) in command:
            return 4, days[4]
        if str(days[5]) in command:
            return 5, days[5]
        if str(days[6]) in command:
            return 6, days[6]
        if any(s.isdigit() for s in command):
            return 404, days[0]
        return 0, days[0]

    def recover_weather(self, command: str) -> str:
        """This function give the weather by use the user input.

        Args:
            command (str): sentence input

        Returns:
            str: The final generated phrase
        """
        success_request =  200
        bad_request = 404
        city = self.recover_city(command)
        day, week_day = self.recover_day(command)
        response = requests.get(self.get_url(city), timeout=8)
        logging.debug(" Response: " + str(response.status_code))
        if str(response.status_code) != success_request:
            response = response.json()
            if day != bad_request:
                main = str(response["daily"]["weathercode"][day])
                max_temp = str(int(response["daily"]["temperature_2m_max"][day]))
                min_temp = str(int(response["daily"]["temperature_2m_min"][day]))
                precipitation = str(response["daily"]["precipitation_probability_max"][day])
                if self.lang != "en":
                    return f" {self.phrase_weather[0]} {city} {self.phrase_weather[1]} {self.utils.number_to_word(str(week_day))} {self.phrase_weather[2]} {self.wwc_weather[main]} {self.phrase_weather[3]} {self.utils.number_to_word(max_temp)} {self.phrase_weather[4]} {self.utils.number_to_word(min_temp)} {self.phrase_weather[5]} {self.utils.number_to_word(precipitation)} {self.phrase_weather[6]}"
                return f" {self.phrase_weather[0]} {city} {self.phrase_weather[1]} {week_day} {self.phrase_weather[2]} {self.wwc_weather[main]} {self.phrase_weather[3]} {max_temp} {self.phrase_weather[4]} {min_temp} {self.phrase_weather[5]} {precipitation} {self.phrase_weather[6]}"
            self.audio.create(file=True, namefile="ErrorDay")
            return ""
        logging.error(" repeat the request or wait a few minutes")
        self.audio.create(file=True, namefile="ErrorMeteo")
        return ""
