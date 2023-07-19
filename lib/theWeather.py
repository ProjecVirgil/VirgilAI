import os
import requests
import json

import deepl

from lib.prefix import Log 

current_path = os.getcwd()
file_path = os.path.join(current_path,'setupAndLaunch/secret.json')

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    weather_key = secrets["weather"]
    deeple_key = secrets["deeple"]
    
translator = deepl.Translator(deeple_key) 
    
#Init the api wheather
def url(CITY):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    url = BASE_URL + "appid=" + weather_key + "&q=" + CITY
    return url



def TheWeather(command:str):
    if(' a ' in command):
        print(Log(" citta scelta corretamente"))
        command=command.split(" a ")[1].strip()
        CITY = command.split(" ")[0]
        print(Log( " Citta selezionata: " + CITY))
    else:
        CITY = "Salerno"    
        print(Log( "Citta di default selezionata: " + CITY))
    print(Log(" weather function"))
    response = requests.get(url(CITY))
    print(Log(" Response: " + str(response.status_code)))
    if(response.status_code != 200):
        print("Ripeti la richiesta o aspetta qualche minuto")
        return None
    else:
        response = response.json()
        main = response['weather'][0]['description']
        out = translator.translate_text(main, target_lang="IT")
        print(print(Log(str(out))))
        stringa = f"A {CITY} il tempo è {out.text}"
        print(f"\nVirgilio: A {CITY} il tempo è {out.text}")
        return stringa
    

    
def Temp(command):
    print(Log(" funzione temp"))
    if(' a ' in command):
        print(Log(" citta scelta corretamente"))
        command=command.split(" a ")[1].strip()
        CITY = command.split(" ")[0]
        print(Log( "Citta selezionata: " + CITY))
    else:
        print(Log( "Citta di default selezionata: " + CITY))
        CITY = "Salerno"    
    
    response = requests.get(url(CITY)).json()
    temp = response['main']['temp'] - 273.15
    tempMax= int(response['main']['temp_max']) - 273.15
    tempMin= int(response['main']['temp_min']) - 273.15
    humidity= int( response['main']['humidity'])
    stringa = f"La temperatura ora a {CITY} è di {int(temp)} gradi, con una massima di {int(tempMax)} gradi, una minima di {int(tempMin)} gradi e un' umidita pari al {humidity}% "
    print(f"\nVirgilio: La temperatura ora a {CITY} è di {int(temp)} gradi, con una massima di {int(tempMax)} gradi, una minima di {int(tempMin)} gradi e un' umidita pari al {humidity}% ")
    return stringa