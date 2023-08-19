"""_summary_

    Returns:
        _type_: _description_
"""
import sys
import json
import time

import openai
from pygame import mixer


from lib.logger import Logger
from lib.sound import Audio # Create
from lib.time import Time  #now,diffTime,conversion
from lib.change_value import  VolumeMixer  #change
from lib.the_weather import Wheather  #recoverWeather
from lib.calendar_rec import Calendar
from lib.the_news import  Newsletter #createNews
from lib.the_light import turn
from lib.searchyt import   MediaPlayer #playMusic
from lib.manage_events import EventScheduler #addEvents

# ---- File for manage all the preset command ----
class CommandSelection:
    """_summary_
    """
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
        #TODO MAKE THE PROMPT IN A FILE
        self.start_prompt = [
                {"role": "system", "content": '''
Sei un assistente virtuale che parla italiano e che scrive i numeri a lettere di nome Virgilio puoi fare essetamente queste cose
-  Creare un timer 
-  Dire il tempo in questo momento 
-  Sai le ultime notizie
-  Cambiare il volume del tuo audio
-  La temperatura esterna
-  Interagisci con la domotica
-  Sai che ore sono
-  Ricordi i miei impegni
-  Poi riprodurre musica da youtube
-  E sai fare un sacco di altre cose come Creare un piano di allenamento, una dieta e tutto cio che puo chiedere un utente

Quando ti chiedono cosa sai fare mi spiegherai questi punti con degli esempi
- Virgilio imposta un timer di 10 minuti
- Virgilio Che tempo fa oggi
- Virgilio imposta il volume a 10%
- Virgilio dimmi le ultime notizie
- Virgilio che temperatura fa
- Virgilio accendi la luce
- Virgilio che ore sono
- Virgilio riproduci nomecanzone a scelta
- Virgilio ricordami che domani ho un impegno
- Virgilio che giorno è domani
eccetera

Se faccio domande relative a uno dei comandi sopra elencati e a cui non sai rispondermi dimmi di provare a dire il comando e usi gli esempi che ti ho elencato prima

Pronto a fingerti Virgilio? rispondi si se hai capito ed da ora in poi quando ti faccio una domanda mi rispondi come se fossi un assistente virtuale'''}
            ]
        with open("setup/settings.json",encoding="utf8") as file:
            secrets = json.load(file)
            self.temeperature= secrets['temperature']
            self.max_token= secrets['max_tokens']
            self.api_key = secrets["openAI"]
        openai.api_key = self.api_key

    #function for communicate whith api GPT-3
    def get_response(self,messages:list):
        """_summary_

        Args:
            messages (list): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" Sto creando la risposta..."), flush=True)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=messages,
            temperature = float(self.temeperature), # 0.0 - 2.0
            max_tokens=int(self.max_token)
        )
        return response.choices[0].message

    #shutdown function
    def off(self):
        """_summary_
        """
        print(self.logger.log(" shut function"), flush=True)
        print("\nVirgilio: Spegnimento in corso...", flush=True)
        with open("connect/res.json", 'w',encoding="utf8") as file:
            data = {
                "0":["spento","spento",False]
            }
            json.dump(data,file,indent=4)
        time.sleep(2)
        sys.exit(0)

    def send_command(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        mixer.init()
        if ("spegniti" in command) or ("spegnimento" in command):
            print(self.logger.log(" pre shut function"),flush=True)
            self.off()
        if (("ore" in command) or ("ora" in command)) and (("sono" in command)or("e'" in command)):
            print(self.logger.log(" pre time function"),flush=True)
            response = self.time.now()
            return response
        if "stop" in command or "fermati" in command or "basta" in command:
            print(self.logger.log(" Audio stopped succesflully"),flush=True)
            mixer.music.stop()
        if "volume" in command and(("imposta")in command or ("metti" in command) or ("inserisci")):
            print(self.logger.log(" pre volume function"),flush=True)
            response = self.volume_mixer.change(command)
            if response == "104":
                print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ",
                      flush=True)
                self.audio.create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
                return None
            return response
        if (("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command) or (("gradi" in command ) or ("temperatura" in command))) and (("quanti" in command) or ("quanta" in command)):
            print(self.logger.log(" pre wheather function"),flush=True)
            response = self.wheather.recover_weather(command)
            return response
        if "timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) ):
            print(self.logger.log(" pre timer function"), flush=True)
            try:
                command = str(command).split(" di ")[1].strip()
                my_time = self.time.conversion(command)
                return str(my_time)
            except IndexError:
                print("Please try the command again", flush=True)
                self.audio.create("Please try the command again") #PRESET
                return None
        if "sveglia" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command)):
            print(self.logger.log(" pre alarm function"),flush=True)
            try:
                time_diff = self.time.diff_time(command)
                print(self.logger.log(f"tempo mancante alla sveglia {time_diff}"), flush=True)
                my_time = self.time.conversion(time_diff)
                print(self.logger.log(f"tempo mancante alla sveglia in secondi {my_time}"), flush=True)
                return str(my_time)
            except IndexError:
                print("Please try the command again",flush=True)
                self.audio.create("Please try the command again") # DA STOSTITURE COL PRESET
                return None
        if "che giorno e" in command or "che giorno della settima e" in command:
            print(self.logger.log(" pre recovery function"),flush=True)
            response=self.calendar.get_date(command)
            return response
        if "quanto mancano alle" in command or "quanto manca alle" in command:
            print(self.logger.log(" pre difftime function"),flush=True)
            response = self.time.diff_time(command)
            return response
        if "quanto manca" in command or "quanti giorni mancano al" in command:
            print(self.logger.log(" pre getDiff function"),flush=True)
            response = self.calendar.get_diff(command)
            return response
        if (("news" in command) or ("novita" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command)):
            print(self.logger.log(" pre news function"),flush=True)
            response = self.news_letter.create_news(command)
            return response
        if "play" in command or "riproduci" in command:
            print(self.logger.log(" pre yt function"),flush=True)
            self.media_player.play_music(command)
        if "ricordami" in command or "imposta un promemoria" in command or "mi ricordi" in command:
            print(self.logger.log(" pre create events function"),flush=True)
            return self.event_scheduler.add_events(command)
        if "luce" in command and (("accendi" in command) or ("spegni" in command)):
            print(self.logger.log(" pre light function"),flush=True)
            turn(command)
            return "Ok"
        else:
            print(self.logger.log(" GPT function"), flush=True)
            self.start_prompt.append({"role": "user", "content": command})
            try:
                new_message = self.get_response(messages=self.start_prompt)
            except:
                print(self.logger.log("Unfortunately the key of openAI you entered is invalid or not present if you don't know how to get a key check the guide on github"), flush=True)
                self.audio.create(file=True,namefile="ErrorOpenAi")
                return#TO REG
            print(self.logger.log(" response created"),flush=True)
            print(f"\nVirgilio: {new_message['content']}",flush=True)
            print(self.logger.log(" I am hanging the command..."),flush=True)
            self.start_prompt.append(new_message)
            print(self.logger.log(" command append"),flush=True)
            return new_message['content']
