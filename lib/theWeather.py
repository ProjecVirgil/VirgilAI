import os
import requests
import json

import deepl

from lib.numberConvertToText import numberToWord
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
        print('ciao')
        print(Log(" city chosen correctly"))
        command=command.split(" a ")[1].strip()
        CITY = command.split(" ")[0]
        print(Log( " selected city: " + CITY))
        return CITY
    else:
        CITY = secrets['city'] 
        print(Log( " default city selected: " + CITY))
        return CITY

def recoverWeather(command:str):
    CITY = recoverCity(command)
    print(Log(" weather function"))
    response = requests.get(url(CITY))
    print(Log(" Response: " + str(response.status_code)))
    if(response.status_code != 200):
        print(Log("repeat the request or wait a few minutes"))
        return "Non riesco a collegarmi al meteo mi dispiace controlla che la chiave o la connesione siano ok"  #TO REG
    else:
        response = response.json()
        main = response['weather'][0]['description']
        try:
            outputTranslation = translator.translate_text(main, target_lang=str(language).upper())
        except:
            print(Log(' Error in the key or connection try later or insert a valid key'))
            return 'Mi dispiace ma purtroppo sembra che o la chiave inserita o la connesione non permattano la traduzione del meteo' #TO REG
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
    
    stringa = f"La temperatura ora a {CITY} è di {numberToWord(temperature)} gradi, con una massima di {numberToWord(tempatureMax)} gradi, una minima di {numberToWord(tempratureMin)} gradi e un' umidita pari al {humidity} percento "
    print(f"\nVirgilio: La temperatura ora a {CITY} è di {temperature} gradi, con una massima di {tempatureMax} gradi, una minima di {tempratureMin} gradi e un' umidita pari al {humidity}% ")
    return stringa
