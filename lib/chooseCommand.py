import sys
import json
import time
import os 

import openai
import pygame


from lib.prefix import Log
from lib.sound import create
from lib.timeNow import now
from lib.changeValue import change
from lib.theWeather import recoverWeather
from lib.timeConv import conversion
from lib.calendarRec import recoverDayOfWeek
from lib.theNews import createNews
from lib.theLight import turn
from lib.searchyt import playonyt

#function for manage the command
#Preset command

#Start contest for GPT-3 API
messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata Virgilio."}
    ]
current_path = os.getcwd()
file_path = os.path.join(current_path,'setting.json')

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    _temperature= secrets['temperature']
    _max_token= secrets['max_tokens']
    api_key = secrets["openAI"]
openai.api_key = api_key


#function for communicate whith api GPT-3
def get_response(messages:list):
    print(Log(" Sto creando la risposta..."))
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = float(_temperature), # 0.0 - 2.0
        max_tokens=int(_max_token)
    )
    return response.choices[0].message

#shutdown function
def off():
    print(Log(" shut function"))
    print("\nVirgilio: Spegnimento in corso...")
    with open("connect/res.json", 'w') as file:
            data = {
                "0":["spento","spento",False]
            }
            json.dump(data,file,indent=4)
    time.sleep(2)
    sys.exit(0)
    
def Sendcommand(command:str):
    pygame.init()
    
    if(("spegniti" in command) or ("spegnimento" in command)):
        print(Log(" pre shut function"))
        off()
        
    elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("è" in command))):
        print(Log(" pre time function"))
        result = now()
        return result

    elif("stop" in command or "fermati" in command or "basta" in command):
        create("va bene mi fermo")
        
    elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
        print(Log(" pre volume function"))
        result = change(command)
        if(result == 104):
            print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ")
            create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
            return None
        else:
            return result

        
    elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command) or (("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command))):
        print(Log(" pre wheather function"))
        result = recoverWeather(command)
        return result
    elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Log(" pre timer function"))
        try:
            command = str(command).split(" di ")[1].strip()
            my_time = conversion(command)
            return my_time
        except IndexError:
            print("Please try the command again")
            create("Please try the command again")
            return None
        
        #timer(command)
    elif("che giorno e" in command or "che giorno della settima e" in command):
        print(Log(" pre recovery function"))
        result=recoverDayOfWeek(command)
        return result
    
    elif(( ("news" in command) or ("novita" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
        print(Log(" pre news function"))
        result = createNews(command)
        return result
    elif("play" in command or "riproduci" in command ):
        playonyt(command)
        print(Log(" pre yt function"))
        
    elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
        print(Log(" pre light function"))
        turn(command)
    #Question at GPT-3   
    else:
        print(Log(" GPT function"))
        messages.append({"role": "user", "content": command})
        try:
            new_message = get_response(messages=messages)
        except:
            print(Log("Unfortunately the key of openAI you entered is invalid or not present if you don't know how to get a key check the guide on github"))
            pygame.mixer.music.unload()    
            pygame.mixer.music.load('asset/ErrorOpenAi.mp3') 
            pygame.mixer.music.play()    #TO REG
        print(Log(" response created"))
        print(f"\nVirgilio: {new_message['content']}")
        print(Log(" I am hanging the command..."))
        messages.append(new_message)
        print(Log(" command append"))
        return new_message['content']
