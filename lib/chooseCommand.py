import sys
import json
import time
import os 

import openai
import pygame


from lib.logger import Logger
from lib.sound import Audio # Create
from lib.time import Time  #now,diffTime,conversion
from lib.changeValue import  VolumeMixer  #change
from lib.theWeather import Wheather  #recoverWeather
from lib.calendarRec import getDate,getDiff
from lib.theNews import  Newsletter #createNews
from lib.theLight import turn
from lib.searchyt import   MediaPlayer #playMusic
from lib.manageEvents import EventScheduler #addEvents

# ---- File for manage all the preset command ----


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
    print(Logger.Log(" Sto creando la risposta..."), flush=True)
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = float(_temperature), # 0.0 - 2.0
        max_tokens=int(_max_token)
    )
    return response.choices[0].message

#shutdown function
def off():
    print(Logger.Log(" shut function"), flush=True)
    print("\nVirgilio: Spegnimento in corso...", flush=True)
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
        print(Logger.Log(" pre shut function"),flush=True)
        off()
    elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("e'" in command))):
        print(Logger.Log(" pre time function"),flush=True)
        response = Time.now()
        return response
    elif("stop" in command or "fermati" in command or "basta" in command):
            print(Logger.Log(" Audio stopped succesflully"),flush=True)
            pygame.mixer.music.stop()
    elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
        print(Logger.Log(" pre volume function"),flush=True)
        response = VolumeMixer.change(command)
        if(response == "104"):
            print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ", flush=True)
            Audio.create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
            return None
        else:
            return response
    elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command) or (("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command))):
        print(Logger.Log(" pre wheather function"),flush=True)
        response = Wheather.recoverWeather(command)
        return response
    elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Logger.Log(" pre timer function"), flush=True)
        try:
            command = str(command).split(" di ")[1].strip()
            my_time = Time.conversion(command)
            return str(my_time)
        except IndexError:
            print("Please try the command again", flush=True)
            Audio.create("Please try the command again") #PRESET
            return None
    elif("sveglia" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Logger.Log(" pre alarm function"),flush=True)
        try:
            timeDiff = Time.diffTime(command)
            print(Logger.Log(f"tempo mancante alla sveglia {timeDiff}"), flush=True)
            my_time = Time.conversion(timeDiff)
            print(Logger.Log(f"tempo mancante alla sveglia in secondi {my_time}"), flush=True)
            return str(my_time)
        except IndexError:
            print("Please try the command again",flush=True)
            Audio.create("Please try the command again") # DA STOSTITURE COL PRESET
            return None
    elif("che giorno e" in command or "che giorno della settima e" in command):
        print(Logger.Log(" pre recovery function"),flush=True)
        response=getDate(command)
        return response
    elif("quanto mancano alle" in command or "quanto manca alle" in command):
         print(Logger.Log(" pre difftime function"),flush=True)
         response = Time.diffTime(command)
         return response   
    elif("quanto manca" in command or "quanti giorni mancano al" in command):
        print(Logger.Log(" pre getDiff function"),flush=True)
        response = getDiff(command)
        return response
    elif(( ("news" in command) or ("novita" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
        print(Logger.Log(" pre news function"),flush=True)
        response = Newsletter.createNews(command)
        return response
    elif("play" in command or "riproduci" in command ):
        print(Logger.Log(" pre yt function"),flush=True)
        MediaPlayer.playMusic(command)
    elif("ricordami" in command or "imposta un promemoria" in command or "mi ricordi" in command):
        print(Logger.Log(" pre create events function"),flush=True)
        return EventScheduler.addEvents(command)
        #TODO SEE WHAT MAKE
    elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
        print(Logger.Log(" pre light function"),flush=True)
        turn(command)
    #Question at GPT-3   
    else:
        print(Logger.Log(" GPT function"), flush=True)
        messages.append({"role": "user", "content": command})
        try:
            new_message = get_response(messages=messages)
        except:
            print(Logger.Log("Unfortunately the key of openAI you entered is invalid or not present if you don't know how to get a key check the guide on github"), flush=True)
            Audio.create(file=True,namefile="ErrorOpenAi")
            return#TO REG
        print(Logger.Log(" response created"),flush=True)
        print(f"\nVirgilio: {new_message['content']}",flush=True)
        print(Logger.Log(" I am hanging the command..."),flush=True)
        messages.append(new_message)
        print(Logger.Log(" command append"),flush=True)
        return new_message['content']
