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
            self.lang = settings["language"]
        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.script_wheather = self.script["wheather"]
            self.phrase = self.script_wheather["phrase"]
            self.split = self.script_wheather["split"]
            self.wwc = self.script_wheather["WWC"]

        self.parole_significato_domani = [
            "domani","futuro", "successivo", "imminente", "prossimo", "successivo", 
            "giorno successivo", "giorno dopo", "prossima giornata", 
            "avvenire", "imminenza", "previsione", "attesa", "prossimità", 
            "incognita", "domani", "giorno successivo", "giorno a venire",
            "dopo","tra due giorni", "il giorno seguente", 
            "successivo al prossimo giorno", "due giorni dopo",
            "il giorno a venire", "dopo il giorno successivo",
            "oggi","in questa giornata", "nella presente giornata", "nella data attuale", 
            "in questo momento", "in questo giorno", "nella giornata in corso"
        ]

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
        if "fa" in command: #SOSTITUIRE POI CON IL FATTO DELLE LINGUE E STARE ATTENTI ALLE TRADUZIONI
            print(self.logger.log(" city chosen correctly"), flush=True)
            try:
                if command[command.index("fa") + 1] in self.parole_significato_domani:
                    city = command[command.index("fa") + 2]
                    print(self.logger.log( " selected city: " + city), flush=True)
                    return city
                city = command[command.index("fa") + 1]
                print(self.logger.log( " selected city: " + city), flush=True)
                return city
            except IndexError:
                city = self.city
                print(self.logger.log( " default city selected: " + city), flush=True)
                return city
        else:
            return self.city #city default

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
        days = self.get_current_week_days() #worka
        if self.split[1] in command or str(days[0]) in command :
            return 0,days[0]
        if self.split[2] in command or str(days[1]) in command:
            return 1,days[1]
        if self.split[3] in command or str(days[2]) in command:
            return 2,days[2]
        if str(days[3]) in command:
            return 3,days[3]
        if str(days[4]) in command:
            return 4,days[4]
        if str(days[5]) in command:
            return 5,days[5]
        if str(days[6]) in command:
            return 6,days[6]
        if any(s.isdigit() for s in command):
            return 404,days[0]
        return 0,days[0]

    def recover_weather(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        city = self.recover_city(command) #worka
        day,week_day = self.recover_day(command) #worka
        print(self.logger.log(" weather function"), flush=True)
        response = requests.get(self.get_url(city),timeout=8)
        print(self.logger.log(" Response: " + str(response.status_code)), flush=True)
        if str(response.status_code) != 200:
            response = response.json()
            if day != 404 :
                main = str(response["daily"]["weathercode"][day])
                max_temp = str(int(response["daily"]["temperature_2m_max"][day]))
                min_temp =  str(int(response["daily"]["temperature_2m_min"][day]))
                precipitation = str(response["daily"]["precipitation_probability_max"][day])
                return f" {self.phrase[0]} {city} {self.phrase[1]} {self.utils.number_to_word(str(week_day))} {self.phrase[2]} {self.wwc[main]} {self.phrase[3]} {self.utils.number_to_word(max_temp)} {self.phrase[4]} {self.utils.number_to_word(min_temp)} {self.phrase[5]} {self.utils.number_to_word(precipitation)} {self.phrase[6]}"
            self.audio.create(file=True,namefile="ErrorDay")
            return ""
        print(self.logger.log(" repeat the request or wait a few minutes"), flush=True)
        self.audio.create(file=True,namefile="ErrorMeteo")
        return ""
