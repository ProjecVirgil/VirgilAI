"""_summary_

    Returns:
        _type_: _description_
    """
import datetime
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
        time_string = f"Sono le {str(hours_to_words)} e {str(minuts_to_words)}  minuti"
        print(time.strftime("\nVirgilio: Sono le %H e %M minuti", time_tuple),flush=True)
        return time_string


    def diff_time(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        current_time = datetime.datetime.now().time()
        #TODO MORE TEST WITH STT
        if " al " in command:
            query=command.split(" al")[1].strip()
        elif " alle " in command:
            query=command.split(" alle")[1].strip()
        elif " per le " in command:
            query=command.split(" le")[1].strip()
        number_find = self.utils.count_number(command)
        if number_find > 1:
            try:
                query_splitted = query.split(" e ")
                hours = query_splitted[0]
                minuts = query_splitted[1]
            except IndexError:
                query_splitted = query.split(":")
                hours = query_splitted[0]
                minuts = query_splitted[1]

        else:
            if "mezza" in command:
                query = query.replace("mezza","30")
                try:
                    query_splitted = query.split(":")
                except:
                    query_splitted = query.split(" e ")
                hours = query_splitted[0]
                minuts = query_splitted[1]
            elif "meno un quarto" in command:
                query = query.replace("meno un quarto", "45")
                query = query.replace(query.split(" ")[0],
                str(int(query.split(" ")[0])-1) ) #TAKE THE NUMBER OF THE NOW AND REPLACE IT WITH ITSELF MINUS ONE
                query_splitted = query.split(" ")
                hours = query_splitted[0]
                minuts = query_splitted[1]
            elif "un quarto" in command:
                query = query.replace("un quarto","15")
                try:
                    query_splitted = query.split(":")
                except:
                    query_splitted = query.split(" e ")
                hours = query_splitted[0]
                minuts = query_splitted[1]
            else:
                minuts = "00"
                hours = query.split(" ")[-1]


        time_string = f"{hours}:{minuts}"

        time_formatted = datetime.datetime.strptime(time_string, "%H:%M").time()

        data_corrente = datetime.datetime.combine(datetime.date.today(), current_time)
        data_specificata = datetime.datetime.combine(datetime.date.today(), time_formatted)

        diff_time = data_specificata - data_corrente

        calculated_hours, rest = divmod(diff_time.seconds, 3600)
        calculated_minuts, calculate_seconds = divmod(rest, 60)

        if "sveglia" in command:
            print(
                self.logger.log(
                f" tempo calcolato per la sveglia {calculated_hours},{calculated_minuts},{calculate_seconds}"),
                flush=True)
            return f"{calculated_hours} ore {calculated_minuts} minuti e {calculate_seconds} secondi"
        print(
            self.logger.log(
            f" alle {self.utils.number_to_word(hours)} e {self.utils.number_to_word(minuts)} mancano {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minuts)} {self.utils.number_to_word(calculate_seconds)}"),flush=True)
        return f" alle {self.utils.number_to_word(hours)} e {self.utils.number_to_word(minuts)} mancano {self.utils.number_to_word(calculated_hours)} ore {self.utils.number_to_word(calculated_minuts)} minuti e {self.utils.number_to_word(calculate_seconds)} secondi"
        # Stampa la differenza in un formato più comprensibile


    def conversion(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" Conversion in progress"),flush=True)
        command=command.replace(","," ")
        command=command.split(" ")

        if(
            (("ora" in command) or ("ore" in command))
            and (("minuto" in command) or ("minuti" in command))
            and (("secondo" in command) or ("secondi" in command))):
            hours=int(command[0])
            minutes = int(command[2])
            seconds = int(command[5])
            sum_seconds= hours*3600 + minutes * 60 + seconds
            return sum_seconds

        if(
            (("ora" in command) or ("ore" in command))
            and (("minuto" in command) or ("minuti" in command)) ):
            hours=int(command[0])
            minutes = int(command[3])
            sum_seconds= hours*3600 + minutes * 60
            return sum_seconds

        if(
            (("minuto" in command) or ("minuti" in command))
            and (("secondo" in command) or ("secondi" in command))):
            minutes=int(command[0])
            seconds = int(command[3])
            sum_seconds= minutes * 60 + seconds
            return sum_seconds

        if(
            (("ora" in command) or ("ore" in command))
            and (("secondo" in command) or ("secondi" in command))):
            hours=int(command[0])
            seconds = int(command[3])
            sum_seconds= hours * 3600 + seconds
            return sum_seconds

        if(((command[1] == 'ore')) or (command[1] == 'ora')):
            return int(command[0])*3600
        if((command[1] == 'minuti') or (command[1] == 'minuto')):
            return int(command[0])*60
        return int(command[0])
