"""_summary_

    Returns:
        _type_: _description_
"""
#TODO add ALL THE STRINGS IN THE JSON

import sys
import json
import time

import openai
from pygame import mixer
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


from lib.logger import Logger
from lib.sound import Audio # Create
from lib.time import Time  #now,diffTime,conversion
from lib.change_value import  VolumeMixer  #change
from lib.the_weather import Wheather  #recoverWeather
from lib.calendar_rec import Calendar
from lib.the_news import  Newsletter #createNews
from lib.searchyt import   MediaPlayer #playMusic
from lib.manage_events import EventScheduler
from lib.utils import Utils #addEvents
#from lib.the_light import turn

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
        self.utils = Utils()
        self.stop_words_it = set(stopwords.words("italian"))

        model_filename = "model/model_it.pkl"
        self.loaded_model = joblib.load(model_filename)
        self.tfidf_vectorizer = joblib.load("model/tfidf_vectorizer_it.pkl")
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
        self.lang = settings["language"]
        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.scritp_command = self.script["command"]
            self.split = self.scritp_command["split"]

        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.scritp_time = self.script["time"]
            self.phrase_time = self.scritp_time["phrase"]
            self.split_time = self.scritp_time["split"]

        #Start contest for GPT-3.5 API
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

Pronto a fingerti Virgilio? rispondi si se hai capito ed da ora in poi quando ti faccio una domanda mi rispondi come se fossi un assistente virtuale'''}]
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
            messages = messages,
            temperature = float(self.temeperature), # 0.0 - 2.0
            max_tokens = int(self.max_token)
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

    def clean(self,command):
        """_summary_
        """
        try:
            filtered_tokens = []
            tokens = word_tokenize(command.lower().strip())
            for word in tokens:
                if word not in self.stop_words_it and word not in (",","?"):
                    filtered_tokens.append(word)
            print(self.logger.log(f" command processed: {filtered_tokens} "), flush=True)
            return filtered_tokens
        except IndexError:
            #If command contain only virgil word
            return command

    def send_command(self,command):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        mixer.init()
        command_converted = self.tfidf_vectorizer.transform([command])
        predictions = self.loaded_model.predict(command_converted)
        command = self.clean(command)
        if (self.split[0] in command) or (self.split[1] in command): #WORKA
            print(self.logger.log(" pre shut function"),flush=True)
            self.off()
            return
        if predictions  == 'OR': #WORKA
            print(self.logger.log(" pre time function"),flush=True)
            response = self.time.now()
            return response
        if self.split[6] in command or self.split[7] in command or self.split[8] in command: #work
            print(self.logger.log(" Audio stopped succesflully"),flush=True)
            mixer.music.stop()
            return
        if predictions == 'VL': #WORKA
            print(self.logger.log(" pre volume function"),flush=True)
            response = self.volume_mixer.change(command)
            if response == "104":
                print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ",
                      flush=True)
                self.audio.create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
                return None
            return response
        if predictions == 'MT': #WORKA
            print(self.logger.log(" pre wheather function"),flush=True)
            response = self.wheather.recover_weather(command)
            return response
        if predictions == 'TM': #WORKA
            for i in command:
                if self.utils.count_number(i) >= 2:
                    print(self.logger.log(" pre clock function"), flush=True)
                    hours,minuts,calculated_hours,calculated_minuts,calculate_seconds = self.time.diff_time(i)
                    time_calculated =f"{calculated_hours} ore {calculated_minuts} minuti {calculate_seconds} secondi".split(" ")
                    my_time = self.time.conversion(list(time_calculated))
                    return str(my_time)
            print(self.logger.log(" pre timer function"), flush=True)
            try:
                my_time = self.time.conversion(command)
                return str(my_time)
            except IndexError:
                print("Please try the command again", flush=True)
                self.audio.create("Per favore prova a ripetere il comando") #PRESET
                return None
        if predictions == "GDS":#WORKA
            print(self.logger.log(" pre recovery function"),flush=True)
            response=self.calendar.get_date(command)
            return response
        if predictions == "MC": #WORKA
            for i in command:
                if self.utils.count_number(i) >= 2:
                    hours,minuts,calculated_hours,calculated_minuts,calculate_seconds = self.time.diff_time(i)
                    print(
                    self.logger.log(
                    f" {self.split_time[1]} {self.utils.number_to_word(hours)} {self.split_time[3]} {self.utils.number_to_word(minuts)} {self.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minuts)} {self.utils.number_to_word(calculate_seconds)}"),flush=True)
                    return f" {self.split_time[1]} {self.utils.number_to_word(hours)} {self.split_time[3]} {self.utils.number_to_word(minuts)} {self.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.phrase_time[1]} {self.utils.number_to_word(calculated_minuts)} {self.phrase_time[2]} {self.utils.number_to_word(calculate_seconds)} {self.phrase_time[3]}"
            result = self.calendar.diff_date(command)
            print("Manca giorno")
            return result
        if predictions == "NW": #worka
            print(self.logger.log(" pre news function"),flush=True)
            response = self.news_letter.create_news(command)
            return response
        if predictions == "MU": #worka
            print(self.logger.log(" pre yt function"),flush=True)
            self.media_player.play_music(command)
            return
        if predictions == "EV": #worka
            print(self.logger.log(" pre create events function"),flush=True)
            return self.event_scheduler.add_events(command)
        print(self.logger.log(" GPT function"), flush=True)
        self.start_prompt.append({"role": "user", "content": "".join(command)})
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

#TODO ADD THE DOMOTIC FUNCTION
'''if self.split[46] in command and ((self.split[47] in command) or (self.split[48] in command)):
            print(self.logger.log(" pre light function"),flush=True)
            turn(command)
            return "Ok"'''