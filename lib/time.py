"""_summary_

    Returns:
        _type_: _description_
    """
import datetime
import json
import time

from lib.logger import Logger
from lib.utils import Utils

# ---- This file get the current time and more ----

class Time:
    """_summary_
    """
    def __init__(self):
        self.logger = Logger()
        self.utils  = Utils()
        with open('setup/settings.json',encoding="utf8") as file:
            settings = json.load(file)

        self.lang = settings["language"]
        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.scritp_time = self.script["time"]
            self.phrase = self.scritp_time["phrase"]
            self.split = self.scritp_time["split"]

    def now(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" Time function"),flush=True)
        time_tuple = time.localtime() # get struct_time
        hours = time.strftime('%H',time_tuple)
        minuts = time.strftime('%M',time_tuple)
        hours_to_words = self.utils.number_to_word(hours)
        minuts_to_words = self.utils.number_to_word(minuts)
        time_string = f"{self.phrase[4]} {str(hours_to_words)} {self.split[3]} {str(minuts_to_words)}  {self.split[11]}"
        print(time.strftime("\nVirgilio: Sono le %H e %M minuti", time_tuple),flush=True)
        return time_string

    def diff_time(self,index_time:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        current_time = datetime.datetime.now().time()
        try:
            query_splitted = index_time.split(":")
            hours = query_splitted[0]
            minuts = query_splitted[1]
        except ValueError:
            query_splitted = index_time.split(" e ")
            hours = query_splitted[0]
            minuts = query_splitted[1]

        time_string = f"{hours}:{minuts}"

        time_formatted = datetime.datetime.strptime(time_string, "%H:%M").time()

        data_corrente = datetime.datetime.combine(datetime.date.today(), current_time)
        data_specificata = datetime.datetime.combine(datetime.date.today(), time_formatted)

        diff_time = data_specificata - data_corrente

        calculated_hours, rest = divmod(diff_time.seconds, 3600)
        calculated_minuts, calculate_seconds = divmod(rest, 60)

        return hours,minuts,calculated_hours,calculated_minuts,calculate_seconds
        # Stampa la differenza in un formato più comprensibile

    def conversion(self,command):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" Conversion in progress"),flush=True)

        hashmap = {
            "s":None,
            "m":None,
            "h":None,
        }

        for index in enumerate(command):
            if command[index].isdigit():
                if command[index+1] in (self.split[9],self.split[10]):
                    hashmap["h"] = command[index]
                elif command[index+1] in ( self.split[11],self.split[12]):
                    hashmap["m"] = command[index]
                elif command[index+1] in (self.split[13],self.split[14]):
                    hashmap["s"] = command[index]

        if (hashmap["h"] is not None) and (hashmap["m"] is not None) and (hashmap["s"] is not None ):
            hours=int(hashmap["h"])
            minutes = int(hashmap["m"])
            seconds = int(hashmap["s"])
            sum_seconds= hours*3600 + minutes * 60 + seconds
            return sum_seconds

        if (hashmap["h"] is not None) and (hashmap["m"] is not None):
            hours=int(hashmap["h"])
            minutes = int(hashmap["m"])
            sum_seconds= hours*3600 + minutes * 60
            return sum_seconds

        if(hashmap["m"] is not None) and (hashmap["s"] is not None):
            minutes=int(hashmap["m"])
            seconds = int(hashmap["s"])
            sum_seconds= minutes * 60 + seconds
            return sum_seconds

        if(hashmap["h"] is not None) and (hashmap["s"] is not None):
            hours=int(hashmap["h"])
            seconds = int(hashmap["s"])
            sum_seconds= hours * 3600 + seconds
            return sum_seconds

        if hashmap["h"] is not None:
            return int(hashmap["h"])*3600
        if hashmap["m"] is not None:
            return int(hashmap["m"])*60

        return int(hashmap["s"])
