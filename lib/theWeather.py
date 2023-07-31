import calendar
import os
import requests
import json
import datetime

from geopy.geocoders import Nominatim

from lib.utils import Utils
from lib.logger import Logger
from lib.sound import Audio 

# ---- This file get the Meteo of all week ----


current_path = os.getcwd()
file_path = os.path.join(current_path,'setting.json')


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

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    city = secrets["city"]
    
  
class Wheather:
    
    def __init__(self) -> None:
        self.logger = Logger()
        self.audio = Audio()
        self.utils  = Utils()
    def get_coordinates(self,city_name):
        geolocator = Nominatim(user_agent="city_locator")
        location = geolocator.geocode(city_name)
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            print(f"Coordinate not found for '{city_name}'", flush=True)
            return None, None   
        
    #Init the api wheather
    def getUrl(self,CITY):
        latitude, longitude = self.get_coordinates(CITY)
        if latitude is not None and longitude is not None:
            url= f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FLondon"
        return url

    def recoverCity(self,command:str):
        if(' a ' in command):
            print(self.logger.Log(" city chosen correctly"), flush=True)
            command=command.split(" a ")[1].strip()
            CITY = command.split(" ")[0]
            print(self.logger.Log( " selected city: " + CITY), flush=True)
            return CITY
        else:
            CITY = city
            print(self.logger.Log( " default city selected: " + CITY), flush=True)
            return CITY

    def get_current_week_days(self):
        today = datetime.date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1] 
        week_days = [min(today.day + i, days_in_month) for i in range(7)]
        repition = 0
        for i in week_days:
            if(i == 31):
                repition += 1
                if(repition >= 2):
                    week_days[7 - repition + 1] = repition - 1
        return week_days

    def isValidDate(self,days,command):
        for i in days:
            if(str(i) in command):
                return True
        return False
        

    def recoverDay(self,command:str):
        days = self.get_current_week_days()
        if("oggi" in command or str(days[0]) in command ):
            return 0,days[0]
        elif("domani" in command or str(days[1]) in command):
            return 1,days[1]
        elif("dopo domani" in command or str(days[2]) in command):
            return 2,days[2]
        elif(str(days[3]) in command):
            return 3,days[3]
        elif(str(days[4]) in command):
            return 4,days[4]
        elif(str(days[5]) in command):
            return 5,days[5]
        elif(str(days[6]) in command):
            return 6,days[6]
        elif(any(s.isdigit() for s in command.split()) ):
            return 404,days[0]
        else:
            return 0,days[0]
        

    def recoverWeather(self,command:str):
        CITY = self.recoverCity(command)
        day,weekDay = self.recoverDay(command)
        print(self.logger.Log(" weather function"), flush=True)
        response = requests.get(self.getUrl(CITY))
        print(self.logger.Log(" Response: " + str(response.status_code)), flush=True)
        if(str(response.status_code) != 200):  
            response = response.json()
            if(day != 404):
                main = response["daily"]["weathercode"][day]
                max = str(int(response["daily"]["temperature_2m_max"][day]))
                min =  str(int(response["daily"]["temperature_2m_min"][day]))
                precipitation = str(response["daily"]["precipitation_probability_max"][day]) 
                return f"Il meteo a {CITY} per il {self.utils.numberToWord(str(weekDay))} prevede {WWC[main]} con una massima di {self.utils.numberToWord(max)} gradi,una minima di {self.utils.numberToWord(min)} gradi e una probabilita di precipitazione del {self.utils.numberToWord(precipitation)} percento"
            else:
                self.audio.create(file=True,namefile="ErrorDay")
                return "" 
        
        else:       
            print(self.logger.Log(" repeat the request or wait a few minutes"), flush=True)
            self.audio.create(file=True,namefile="ErrorMeteo")  
            return ""
