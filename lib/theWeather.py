import os
import requests
import json

import deepl

from lib.prefix import Log 

current_path = os.getcwd()
file_path = os.path.join(current_path,'setting.json')

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    weather_key = secrets["weather"]
    deeple_key = secrets["deeple"]
    language = secrets['language']
    
translator = deepl.Translator(deeple_key) 
    
#Init the api wheather
def url(CITY):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    url = BASE_URL + "appid=" + weather_key + "&q=" + CITY
    return url

def recoverCity(command:str):
    
    if(' a ' in command):
        print(Log(" city chosen correctly"))
        command=command.split(" a ")[1].strip()
        CITY = command.split(" ")[0]
        print(Log( " selected city: " + CITY))
    else:
        print(Log( " defalut city selected: " + CITY))
        CITY = secrets['city']   
    
    return CITY

def recoverWeather(command:str):
    CITY = recoverCity(command)
    print(Log(" weather function"))
    response = requests.get(url(CITY))
    print(Log(" Response: " + str(response.status_code)))
    if(response.status_code != 200):
        print(Log(" repeat the request or wait a few minutes"))
        return None
    else:
        response = response.json()
        main = response['weather'][0]['description']
        outputTranslation = translator.translate_text(main, target_lang=str(language).upper())
        print(print(Log(str(outputTranslation))))
        stringa = f"A {CITY} il tempo è {outputTranslation.text}"
        print(f"\nVirgilio: A {CITY} il tempo è {outputTranslation.text}")
        return stringa
    

    
def recoverTemp(command):
    print(Log(" function recoverTemp"))
    CITY = recoverCity(command)
    response = requests.get(url(CITY)).json()
    temperature = response['main']['temp'] - 273.15
    tempatureMax= int(response['main']['temp_max']) - 273.15
    tempratureMin= int(response['main']['temp_min']) - 273.15
    humidity= int( response['main']['humidity'])
    stringa = f"La temperatura ora a {CITY} è di {int(temperature)} gradi, con una massima di {int(tempatureMax)} gradi, una minima di {int(tempratureMin)} gradi e un' umidita pari al {humidity}% "
    print(f"\nVirgilio: La temperatura ora a {CITY} è di {int(temperature)} gradi, con una massima di {int(tempatureMax)} gradi, una minima di {int(tempratureMin)} gradi e un' umidita pari al {humidity}% ")
    return stringa