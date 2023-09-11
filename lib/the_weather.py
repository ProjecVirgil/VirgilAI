""""""
import calendar
import datetime

import csv
import requests

from lib import Settings
from lib.utils import Utils
from lib.logger import Logger
from lib.sound import Audio

# ---- This file get the Meteo of all week ----

class Wheather:
    """
    This class manage to get the wheater for a specific day and time
    """
    def __init__(self) -> None:
        self.logger = Logger()
        self.audio = Audio()
        self.utils  = Utils()
        self.settings = Settings()

        self.city = self.settings.city
        self.lang = self.settings.language

    #Init the api wheather
    def get_url(self,city) -> str:
        """
        This function init the url with the parameters to call the API weather

        Args:
            city (_type_): The city from which the url is obtained 

        Returns:
            url: The final url generated
        """
        latitude, longitude = self.utils.get_coordinates(city)
        if latitude is not None and longitude is not None:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FLondon"
        return url

    def recover_city(self,command:list) -> str:
        """
        This method will be used to recover the city name from sentence

        Args:
            command (str): sentence

        Returns:
            str: City chooise if the city not specify
        """
        MINUM_ACCURACY = 3
        result_list = []
        for word in command:
            min = 100000000
            city = ""
            latitude, longitude = self.utils.get_coordinates(word)
            if latitude is not None and longitude is not None:
                with open("assets/worldcities.csv", 'r',encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=';')
                    for row in csvreader:
                        if(row[0] == "city"):
                            continue
                        result = self.utils.haversine_distance((latitude,longitude), (float(row[2]),float(row[3])))
                        if(result < min):
                            min = result
                            city = row[1]
                    result_list.append((city,min))
        result_list = sorted(result_list, key=lambda x: x[1])
        
        if(result_list[0][1] < MINUM_ACCURACY):
            city_correct = result_list[0][0]
            print(self.logger.log(f" City in the phrase choosen: {city_correct}"))
            return city_correct
        else:
            print(self.logger.log(" Default city choose"))
            return self.city

    def get_current_week_days(self)  -> list:
        """
        This function returns a current week

        Returns:
            list: the week days
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
        """
        This function checks that the date given by user is valid or not and it also check that the day of the month is correct

        Args:
            days (_type_): A list of day in the months
            command (_type_): 

        Returns:
            bool: Valid/Not Valid
        """
        for i in days:
            if str(i) in command:
                return True
        return False

    def recover_day(self,command:str) -> tuple:
        """
        This function recovers the day from the user input

        Args:
            command (str): sentence

        Returns:
            tuple: Index of day and the day
        """
        days = self.get_current_week_days() #worka
        if self.settings.split_wheather[1] in command or str(days[0]) in command :
            return 0,days[0]
        if self.settings.split_wheather[2] in command or str(days[1]) in command:
            return 1,days[1]
        if self.settings.split_wheather[3] in command or str(days[2]) in command:
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

    def recover_weather(self,command:str) -> str:
        """
        This function give the wheather by use the user input

        Args:
            command (str): sentence input

        Returns:
            str: The final generated phrase
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
                if self.lang != "en":
                    return f" {self.settings.phrase_wheather[0]} {city} {self.settings.phrase_wheather[1]} {self.utils.number_to_word(str(week_day))} {self.settings.phrase_wheather[2]} {self.settings.wwc_wheather[main]} {self.settings.phrase_wheather[3]} {self.utils.number_to_word(max_temp)} {self.settings.phrase_wheather[4]} {self.utils.number_to_word(min_temp)} {self.settings.phrase_wheather[5]} {self.utils.number_to_word(precipitation)} {self.settings.phrase_wheather[6]}"
                return f" {self.settings.phrase_wheather[0]} {city} {self.settings.phrase_wheather[1]} {week_day} {self.settings.phrase_wheather[2]} {self.settings.wwc_wheather[main]} {self.settings.phrase_wheather[3]} {max_temp} {self.settings.phrase_wheather[4]} {min_temp} {self.settings.phrase_wheather[5]} {precipitation} {self.settings.phrase_wheather[6]}"
            self.audio.create(file=True,namefile="ErrorDay")
            return ""
        print(self.logger.log(" repeat the request or wait a few minutes"), flush=True)
        self.audio.create(file=True,namefile="ErrorMeteo")
        return ""
