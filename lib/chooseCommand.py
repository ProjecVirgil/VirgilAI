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
from lib.calendarRec import Calendar
from lib.theNews import  Newsletter #createNews
from lib.theLight import turn
from lib.searchyt import   MediaPlayer #playMusic
from lib.manageEvents import EventScheduler #addEvents

# ---- File for manage all the preset command ----
class CommandSelection:
    def __init__(self) -> None:
        self.logger = Logger()
        self.audio = Audio()
        self.time = Time()
        self.volume_mixer = VolumeMixer()
        self.wheather = Wheather()
        self.news_letter = Newsletter()
        self.media_player = MediaPlayer()
        self.event_scheduler = EventScheduler()
        self.calendar = Calendar()
        #Start contest for GPT-3 API
        self.startPrompt = [
                {"role": "system", "content": "Sei un assistente virtuale chiamata Virgilio."}
            ]
        with open("setup/settings.json") as f:
            SECRETS = json.load(f)
            self.TEMPERATURE= SECRETS['temperature']
            self.MAX_TOKEN= SECRETS['max_tokens']
            self.API_KEY = SECRETS["openAI"]
        openai.api_key = self.API_KEY
        
        
    #function for communicate whith api GPT-3
    def get_response(self,messages:list):
        print(self.logger.Log(" Sto creando la risposta..."), flush=True)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=messages,
            temperature = float(self.TEMPERATURE), # 0.0 - 2.0
            max_tokens=int(self.MAX_TOKEN)
        )
        return response.choices[0].message

    #shutdown function
    def off(self):
        print(self.logger.Log(" shut function"), flush=True)
        print("\nVirgilio: Spegnimento in corso...", flush=True)
        with open("connect/res.json", 'w') as file:
                data = {
                    "0":["spento","spento",False]
                }
                json.dump(data,file,indent=4)
        time.sleep(2)
        sys.exit(0)
        
    def Sendcommand(self,command:str):
        pygame.init()
        if(("spegniti" in command) or ("spegnimento" in command)):
            print(self.logger.Log(" pre shut function"),flush=True)
            self.off()
        elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("e'" in command))):
            print(self.logger.Log(" pre time function"),flush=True)
            response = self.time.now()
            return response
        elif("stop" in command or "fermati" in command or "basta" in command):
                print(self.logger.Log(" Audio stopped succesflully"),flush=True)
                pygame.mixer.music.stop()
        elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
            print(self.logger.Log(" pre volume function"),flush=True)
            response = self.volume_mixer.change(command)
            if(response == "104"):
                print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ", flush=True)
                self.audio.create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
                return None
            else:
                return response
        elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command) or (("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command))):
            print(self.logger.Log(" pre wheather function"),flush=True)
            response = self.wheather.recoverWeather(command)
            return response
        elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
            print(self.logger.Log(" pre timer function"), flush=True)
            try:
                command = str(command).split(" di ")[1].strip()
                my_time = self.time.conversion(command)
                return str(my_time)
            except IndexError:
                print("Please try the command again", flush=True)
                self.audio.create("Please try the command again") #PRESET
                return None
        elif("sveglia" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
            print(self.logger.Log(" pre alarm function"),flush=True)
            try:
                timeDiff = self.time.diffTime(command)
                print(self.logger.Log(f"tempo mancante alla sveglia {timeDiff}"), flush=True)
                my_time = self.time.conversion(timeDiff)
                print(self.logger.Log(f"tempo mancante alla sveglia in secondi {my_time}"), flush=True)
                return str(my_time)
            except IndexError:
                print("Please try the command again",flush=True)
                self.audio.create("Please try the command again") # DA STOSTITURE COL PRESET
                return None
        elif("che giorno e" in command or "che giorno della settima e" in command):
            print(self.logger.Log(" pre recovery function"),flush=True)
            response=self.calendar.getDate(command)
            return response
        elif("quanto mancano alle" in command or "quanto manca alle" in command):
            print(self.logger.Log(" pre difftime function"),flush=True)
            response = self.time.diffTime(command)
            return response   
        elif("quanto manca" in command or "quanti giorni mancano al" in command):
            print(self.logger.Log(" pre getDiff function"),flush=True)
            response = self.calendar.getDiff(command)
            return response
        elif(( ("news" in command) or ("novita" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
            print(self.logger.Log(" pre news function"),flush=True)
            response = self.news_letter.createNews(command)
            return response
        elif("play" in command or "riproduci" in command ):
            print(self.logger.Log(" pre yt function"),flush=True)
            self.media_player.playMusic(command)
        elif("ricordami" in command or "imposta un promemoria" in command or "mi ricordi" in command):
            print(self.logger.Log(" pre create events function"),flush=True)
            return self.event_scheduler.addEvents(command)
            #TODO SEE WHAT MAKE
        elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
            print(self.logger.Log(" pre light function"),flush=True)
            turn(command)
        #Question at GPT-3   
        else:
            print(self.logger.Log(" GPT function"), flush=True)
            self.startPrompt.append({"role": "user", "content": command})
            try:
                new_message = self.get_response(messages=self.startPrompt)
            except:
                print(self.logger.Log("Unfortunately the key of openAI you entered is invalid or not present if you don't know how to get a key check the guide on github"), flush=True)
                self.audio.create(file=True,namefile="ErrorOpenAi")
                return#TO REG
            print(self.logger.Log(" response created"),flush=True)
            print(f"\nVirgilio: {new_message['content']}",flush=True)
            print(self.logger.Log(" I am hanging the command..."),flush=True)
            self.startPrompt.append(new_message)
            print(self.logger.Log(" command append"),flush=True)
            return new_message['content']
