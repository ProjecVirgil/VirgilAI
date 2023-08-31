"""_summary_

    Returns:
        _type_: _description_
"""
import calendar
import datetime
import json

from lib.sound import Audio
from lib.logger import Logger
from lib.utils import Utils

# ---- File for get the week of the day ----
class Calendar:
    """_summary_
    """
    def __init__(self) -> None:
        self.utils =Utils()
        self.logger = Logger()
        self.audio = Audio()
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
        self.lang = settings["language"]
        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.scritp_time = self.script["calendar"]
            self.phrase = self.scritp_time["phrase"]
            self.split = self.scritp_time["split"]
            self.months = self.scritp_time["month"]
            self.week = self.scritp_time["week"]
        #self.utils = Utils()
        self.parole_significato_domani = [
            "domani","futuro", "successivo", "imminente", "prossimo", "successivo", 
            "giorno successivo", "giorno dopo", "prossima giornata", 
            "avvenire", "imminenza", "previsione", "attesa", "prossimità", 
            "incognita", "domani", "giorno successivo", "giorno a venire",
            "dopo",
        ]

        self.mesi_dell_anno = [
        "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"
        ]

        self.parole_significato_dopo_domani = [
            "dopo domani","tra due giorni", "il giorno seguente", 
            "successivo al prossimo giorno", "due giorni dopo",
            "il giorno a venire", "dopo il giorno successivo"
        ]

        self.parole_significato_ieri = [
            "ieri","giornata precedente", "il giorno prima", "nell'ultimo giorno", 
        "giorno scorso", "nel passato giorno", "un giorno fa"
        ]

        self.parole_significato_oggi = [
            "oggi","in questa giornata", "nella presente giornata", "nella data attuale", 
            "in questo momento", "in questo giorno", "nella giornata in corso"
        ]

    def clear_number(self,day:str,month:str):
        """_summary_

        Args:
            day (str): _description_
            month (str): _description_

        Returns:
            _type_: _description_
        """
        day = int(day)
        month = int(month)
        day = str(day)
        month = str(month)
        return day,month

    def gen_phrase(self,date):
        """_summary_

        Args:
            date (_type_): _description_

        Returns:
            _type_: _description_
        """
        day,month,year = date.split("-")
        day,month = self.clear_number(day,month)
        index_week = self.index_day_of_week(year,month,day)
        print(f" {self.split[0]} {day} {self.split[1]} {self.months[int(month)-1]} {self.split[2]} {year} {self.split[3]} {self.week[index_week]}",
              flush=True)
        if (day is None or day == '') or month is None or year is None:
            print("I'm sorry but I couldn't get the date right you can reapply",
                  flush=True)
            self.audio.create(file=True,namefile="ErrorDate")
        else:
            if(day != 1 or day != 11):
                return f"{self.split[0]} {self.utils.number_to_word(str(day))} {self.split[1]} {self.months[int(month)-1]} {self.split[2]} {self.utils.number_to_word(str(year))} {self.split[3]} {str(self.week[index_week])}"
            return f"{self.split[6]}{self.utils.number_to_word(str(day))} {self.split[1]} {self.months[int(month)-1]} {self.split[2]} {self.utils.number_to_word(str(year))} {self.split[3]} {str(self.week[index_week])}"
        return None    

    def index_day_of_week(self,year:int,month:int,day:int):
        """_summary_

        Args:
            year (int): _description_
            month (int): _description_
            day (int): _description_

        Returns:
            _type_: _description_
        """
        year = int(year)
        month = int(month)
        day = int(day)
        index = 0
        for week in calendar.monthcalendar(year,month):
            for days in week:
                if days == day:
                    index=week.index(days)
        return index

    def recover_date(self,sentence):
        """_summary_

        Args:
            sentence (_type_): _description_

        Returns:
            _type_: _description_
        """
        count_of_number = self.utils.count_number(sentence)
        if count_of_number == 2:
            year = sentence[-1]
            month = self.months.index(sentence[len(sentence) - 2]) + 1
            day = sentence[len(sentence) - 3]
            return f"{day}-{month}-{year}"
        if(count_of_number  == 1 and self.check_month(sentence)):
            today_date  = datetime.datetime.now().date()
            month = self.months.index(sentence[-1]) + 1
            day = sentence[len(sentence) - 2]
            return f"{day}-{month}-{today_date.year}"
        if(count_of_number  == 1 and not self.check_month(sentence)):
            today_date  = datetime.datetime.now().date()
            day = sentence[-1]
            return f"{day}-{today_date.month}-{today_date.year}"
        #TODO DA FARE POI CON AUDIO
        return "Mi dispiace c'è stato un errore di qualche tipo"

    def check_month(self,sentence):
        """_summary_

        Args:
            sentence (_type_): _description_

        Returns:
            _type_: _description_
        """
        for word in sentence:
            if word in self.mesi_dell_anno:
                return True
        return False

    def recov_preset_date(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        pattern = "%d-%m-%Y"
        if any(elem in self.parole_significato_dopo_domani  for elem in command):
            today = datetime.datetime.today()
            after_tomorrow = today + datetime.timedelta(days=2)
            formatted_date = after_tomorrow.strftime(pattern)
            return formatted_date
        if  any(elem in self.parole_significato_domani  for elem in command):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            formatted_date = tomorrow.strftime(pattern)
            return formatted_date
        if any(elem in self.parole_significato_ieri  for elem in command):
            today = datetime.datetime.today()
            yesterday = today + datetime.timedelta(days=-1)
            formatted_date = yesterday.strftime(pattern)
            return formatted_date
        if any(elem in self.parole_significato_oggi  for elem in command):
            today = datetime.datetime.today()
            today = today + datetime.timedelta(days=0)
            formatted_date = today.strftime(pattern)
            return formatted_date
        return None

    def diff_date(self,command):
        """_summary_

        Args:
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        preset_date  = self.recov_preset_date(command)
        if preset_date is None:
            date = self.recover_date(command)
        elif self.utils.count_number("".join(command)) > 0:
            date = self.recover_date(command)
            date[0] = date[0] + 1
            date = "-".join(date)
        else:
            date = preset_date

        day,month,year = date.split("-")
        day,month = self.clear_number(day,month)
        correct_date = datetime.datetime(int(year), int(month), int(day))
        diff_days = (datetime.datetime.now() - correct_date).days
        print(self.logger.log(
            f"result: {self.phrase[0]} {day} {month} {year} {self.phrase[2]} {diff_days * -1}"),
              flush=True)
        if diff_days * -1 == 1:
            return f" {self.phrase[0]} {self.utils.number_to_word(day)} {self.utils.number_to_word(month)} {self.utils.number_to_word(year)} {self.phrase[1]}"
        return f" {self.phrase[0]} {self.utils.number_to_word(day)}, {self.utils.number_to_word(month)}, {self.utils.number_to_word(year)} {self.phrase[2]} {self.utils.number_to_word(diff_days * -1)} {self.phrase[3]}"

    def get_date(self,command):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        preset_date  = self.recov_preset_date(command)
        if preset_date is None:
            date = self.recover_date(command)
            output = self.gen_phrase(date)
            return output
        if self.utils.count_number("".join(command)) > 0:
            date = self.recover_date(command)
            date[0] = date[0] + 1
            date = "-".join(date)
            output = self.gen_phrase(date)
            return output
        output = self.gen_phrase(preset_date)
        return output
