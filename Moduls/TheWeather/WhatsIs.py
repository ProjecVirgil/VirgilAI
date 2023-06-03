from prefix.creation import Log 

import requests
import json
from googletrans import Translator
translator=Translator()



#Open file whith key api openai
with open("F:\ProjectDante\secret.json") as f:
    secrets = json.load(f)
    weather_key = secrets["weather"]
    
#Init the api wheather
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
CITY = "Napoli"

url = BASE_URL + "appid=" + weather_key + "&q=" + CITY



def TheWeather(command:str):
    if(' a ' in command):
        print(Log(" citta scelta corretamente"))
        command=command.split(" a ")[1].strip()
        CITY = command.split(" ")[0]
        print(CITY)
        
    print(Log(" weather function"))
    response = requests.get(url).json()
    main = response['weather'][0]['description']
    out=translator.translate(main,dest='it')
    stringa = f"A {CITY} il tempo è {out.text}"
    print(f"\nDante: A {CITY} il tempo è {out.text}")
    return stringa
    
    
    
def Temp():
    print(Log(" funzione temp"))
    response = requests.get(url).json()
    temp = response['main']['temp'] - 273.15
    tempMax= int(response['main']['temp_max']) - 273.15
    tempMin= int(response['main']['temp_min']) - 273.15
    humidity= int( response['main']['humidity'])
    stringa = f"La temperatura ora a {CITY} è di {int(temp)} gradi, con una massima di {int(tempMax)} gradi, una minima di {int(tempMin)} gradi e un' umidita pari al {humidity}% "
    print(f"\nOrdis: La temperatura ora a {CITY} è di {int(temp)} gradi, con una massima di {int(tempMax)} gradi, una minima di {int(tempMin)} gradi e un' umidita pari al {humidity}% ")
    return stringa