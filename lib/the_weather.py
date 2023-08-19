"""_summary_

    Returns:
        _type_: _description_
"""
import calendar
import json
import datetime

import requests
from geopy.geocoders import Nominatim

from lib.utils import Utils
from lib.logger import Logger
from lib.sound import Audio

# ---- This file get the Meteo of all week ----


WWC = {
    0: "Cielo sereno",
    1: "Prevalentemente sereno",
    2: "Parzialmente nuvoloso",
    3: "Coperto",
    45: "Nebbia e brina",
    48: "Nebbia e brina",
    51: "Pioggerella leggera",
    53: "Pioggerella moderata",
    55: "Pioggerella intensa",
    56: "Pioggerella ghiacciata leggera",
    57: "Pioggerella ghiacciata intensa",
    61: "Pioggia leggera",
    63: "Pioggia moderata",
    65: "Pioggia intensa",
    66: "Pioggia ghiacciata leggera",
    67: "Pioggia ghiacciata intensa",
    71: "Nevicata leggera",
    73: "Nevicata moderata",
    75: "Nevicata intensa",
    77: "Granelli di neve",
    80: "Rovesci di pioggia leggeri",
    81: "Rovesci di pioggia moderati",
    82: "Rovesci di pioggia violenti",
    85: "Rovesci di neve leggeri",
    86: "Rovesci di neve intensi",
    95: "Temporale leggero o moderato",
    96: "Temporale con grandine leggera",
    99: "Temporale con grandine intensa"
}

class Wheather:
    """_summary_
    """
    def __init__(self) -> None:
        self.logger = Logger()
        self.audio = Audio()
        self.utils  = Utils()
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
            self.city = settings["city"]

    def get_coordinates(self,city_name):
        """_summary_

        Args:
            city_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        geolocator = Nominatim(user_agent="city_locator")
        location = geolocator.geocode(city_name)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        print(f"Coordinate not found for '{city_name}'", flush=True)
        return None, None

    #Init the api wheather
    def get_url(self,city):
        """_summary_

        Args:
            CITY (_type_): _description_

        Returns:
            _type_: _description_
        """
        latitude, longitude = self.get_coordinates(city)
        if latitude is not None and longitude is not None:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FLondon"
        return url

    def recover_city(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        if ' a ' in command:
            print(self.logger.log(" city chosen correctly"), flush=True)
            command=command.split(" a ")[1].strip()
            city = command.split(" ")[0]
            print(self.logger.log( " selected city: " + city), flush=True)
            return city
        city = self.city
        print(self.logger.log( " default city selected: " + city), flush=True)
        return city

    def get_current_week_days(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        today = datetime.date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        week_days = [min(today.day + i, days_in_month) for i in range(7)]
        repition = 0
        for i in week_days:
            if i == 31:
                repition += 1
                if repition >= 2:
                    week_days[7 - repition + 1] = repition - 1
        return week_days

    def is_valid_date(self,days,command):
        """_summary_

        Args:
            days (_type_): _description_
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        for i in days:
            if str(i) in command:
                return True
        return False

    def recover_day(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        days = self.get_current_week_days()
        if "oggi" in command or str(days[0]) in command :
            return 0,days[0]
        if "domani" in command or str(days[1]) in command:
            return 1,days[1]
        if "dopo domani" in command or str(days[2]) in command:
            return 2,days[2]
        if str(days[3]) in command:
            return 3,days[3]
        if str(days[4]) in command:
            return 4,days[4]
        if str(days[5]) in command:
            return 5,days[5]
        if str(days[6]) in command:
            return 6,days[6]
        if any(s.isdigit() for s in command.split()):
            return 404,days[0]
        return 0,days[0]

    def recover_weather(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        city = self.recover_city(command)
        day,week_day = self.recover_day(command)
        print(self.logger.log(" weather function"), flush=True)
        response = requests.get(self.get_url(city),timeout=8)
        print(self.logger.log(" Response: " + str(response.status_code)), flush=True)
        if str(response.status_code) != 200:
            response = response.json()
            if day != 404 :
                main = response["daily"]["weathercode"][day]
                max_temp = str(int(response["daily"]["temperature_2m_max"][day]))
                min_temp =  str(int(response["daily"]["temperature_2m_min"][day]))
                precipitation = str(response["daily"]["precipitation_probability_max"][day])
                return f"Il meteo a {city} per il {self.utils.number_to_word(str(week_day))} prevede {WWC[main]} con una massima di {self.utils.number_to_word(max_temp)} gradi,una minima di {self.utils.number_to_word(min_temp)} gradi e una probabilita di precipitazione del {self.utils.number_to_word(precipitation)} percento"
            self.audio.create(file=True,namefile="ErrorDay")
            return ""
        print(self.logger.log(" repeat the request or wait a few minutes"), flush=True)
        self.audio.create(file=True,namefile="ErrorMeteo")
        return ""
