""""""
import string
import sys
import json
import time

import openai
from pygame import mixer
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from lib import Settings
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

# TODO LIST: 
# - Check some bugs
# - Test the englis version


# ---- File for manage all the preset command ----
class CommandSelection:
    """
    This class is used to select a specific function of the assistant.
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
        self.settings = Settings()

        model_filename = f"model/model_{self.settings.language}.pkl"
        self.loaded_model = joblib.load(model_filename)
        
        self.lang = self.settings.language
        
        if(self.lang == 'it'):
            self.stop_words = set(stopwords.words("italian"))
        else:
            self.stop_words = set(stopwords.words("english"))
        
        # Caratteri di punteggiatura originali
        original_punctuation = string.punctuation
            # Caratteri di punteggiatura che desideri mantenere (per esempio, punto e virgola e punto esclamativo)
        exceptions =  ":'"
            # Crea una nuova stringa di punteggiatura rimuovendo le eccezioni
        self.custom_punctuation = "".join([char for char in original_punctuation if char not in exceptions])

        #Start prompt for GPT-3.5 API
        self.start_prompt = [
                {"role": "system", "content": self.settings.prompt}]
        self.temperature= self.settings.temperature
        self.max_token= self.settings.max_tokens
        self.api_key = self.settings.openai
        openai.api_key = self.api_key

    #function for communicate whith api GPT-3
    def get_response(self,messages:list):
        """_summary_

        Args:
            messages (list): The contest of conversation

        Returns:
            str: The response at the message from gpt
        """
        print(self.logger.log(" I am creating the answer..."), flush=True)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages,
            temperature = float(self.temeperature), # 0.0 - 2.0
            max_tokens = int(self.max_token)
        )
        return response.choices[0].message

    def off(self) -> None:
        """
        Function to shutdown all services and close connection with database
        """
        print(self.logger.log(" shut function"), flush=True)
        print("\nVirgil: Shutdown in progress...", flush=True)
        with open("connect/res.json", 'w',encoding="utf8") as file:
            data = {
                "0":["spento","spento",False]
            }
            json.dump(data,file,indent=4)
        time.sleep(2)
        sys.exit(0)

    def clean(self,command:str,type:str) -> str:
        """
        Function that cleans a command 

        Args:
            command (str): the command to clean
            type (str): type of cleaning model(cleaning the command for work with the models) work (cleaning the command for work with the my code)

        Returns:
            str: The command cleaned
        """
        try:
            if(type == 'model'):
                # Convert text to lowercase
                command = command.lower()
                # Remove punctuation
                command = command.translate(str.maketrans(' ', ' ', self.custom_punctuation))
                # Remove stopwords and lemmatize the words
                words = command.split()
                return ' '.join(words)
            elif(type == 'work'):
                filtered_tokens = []
                tokens = word_tokenize(command.lower().strip())
                for word in tokens:
                    if word not in (",","?") and word not in self.stop_words:
                        filtered_tokens.append(word)
                print(self.logger.log(f" command processed: {filtered_tokens} "), flush=True)
                return filtered_tokens
        except IndexError:
            #If command contain only virgil word
            return command

    def send_command(self,command) -> str:
        """
        Function to process a command received by user

        Args:
            command (str): command cleaned 
            command (str): command cleaned 

        Returns:
            str: The response at the command 
            str: The response at the command 
        """
        mixer.init()
        predictions = self.loaded_model.predict([self.clean(command,"model")])
        command = self.clean(command,"work")
        if (self.settings.split_command[0] in command) or (self.settings.split_command[1] in command): #WORKA
            print(self.logger.log(" pre shut function"),flush=True)
            self.off()
            return
        if predictions  == 'OR': #WORKA
            print(self.logger.log(" pre time function"),flush=True)
            response = self.time.now()
            return response
        if self.settings.split_command[6] in command or self.settings.split_command[7] in command or self.settings.split_command[8] in command: #work
            print(self.logger.log(" Audio stopped succesflully"),flush=True)
            mixer.music.stop()
            return
        if predictions == 'VL': #WORKA
            print(self.logger.log(" pre volume function"),flush=True)
            response = self.volume_mixer.change(command)
            if response == "104":
                print("\nVirgil: You cannot give a value less than 10, you can only give values from 100 to 10",
                      flush=True)
                self.audio.create(file=True,namefile="ErrorValueVolume")
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
                self.audio.create(file=True,namefile="GenericError") #PRESET
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
                    f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minuts)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minuts)} {self.utils.number_to_word(calculate_seconds)}"),flush=True)
                    return f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minuts)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.settings.phrase_time[1]} {self.utils.number_to_word(calculated_minuts)} {self.settings.phrase_time[2]} {self.utils.number_to_word(calculate_seconds)} {self.settings.phrase_time[3]}"
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