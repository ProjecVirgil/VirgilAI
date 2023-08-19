"""_summary_

    Returns:
        _type_: _description_
"""
import calendar
from datetime import datetime as datedate
import datetime


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
        self.months=["gennaio","febbraio","marzo","aprile","maggio","giugno",
                "luglio","agosto","settembre","ottobre","novembre","dicembre"]
        self.week = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]
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
        print(f"Il {day} di {self.months[int(month)-1]} del {year} è {self.week[index_week]}",
              flush=True)
        if (day is None or day == '') or month is None or year is None:
            print("Mi dispiace ma non sono riuscito a capire bene la data puoi rifare la domanda",
                  flush=True)
            self.audio.create(file=True,namefile="ErrorDate")
        else:
            if(day != 1 or day != 11):
                return f"Il {self.utils.number_to_word(str(day))} di {self.months[int(month)-1]} del {self.utils.number_to_word(str(year))} è {str(self.week[index_week])}"
            return f"L'{self.utils.number_to_word(str(day))} di {self.months[int(month)-1]} del {self.utils.number_to_word(str(year))} è {str(self.week[index_week])}"
        return None
    def recov_month(self,query:str):
        """_summary_

        Args:
            query (str): _description_

        Returns:
            _type_: _description_
        """

        query = query.lower()
        for month in self.months:
            if month in query:
                if len(str(self.months.index(month)+1)) == 1:
                    month_replace = "0" + str(self.months.index(month)+1)
                else:
                    month_replace = str(self.months.index(month)+1)
                query = query.replace(month,month_replace)
        return query

    def recov_date(self,query:str):
        """_summary_

        Args:
            query (str): _description_

        Returns:
            _type_: _description_
        """
        patterns = ["%d %m %Y","%d %m","%d"]
        date_current = datedate.now()
        formatted_date = date_current.strftime('%d-%m-%Y')
        query = self.recov_month(query)
        for pattern in patterns:
            try:
                parsed_datetime = datedate.strptime(query, pattern)
                parsed_datetime = parsed_datetime.strftime('%d-%m-%Y')
                if patterns.index(pattern) == 1:
                    parsed_datetime = parsed_datetime.replace("1900",formatted_date.split("-")[2])
                    print(parsed_datetime,"1")
                    return parsed_datetime
                if patterns.index(pattern) == 2:
                    parsed_datetime = parsed_datetime.replace("01",formatted_date.split("-")[1])
                    parsed_datetime = parsed_datetime.replace("1900",formatted_date.split("-")[2])
                    return parsed_datetime
                return parsed_datetime
            except ValueError:
                pass
        return None

    def split_command(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            if " il " in command or "il " in command:
                query=command.split("il")[1].strip()
            elif "l'" in command or "l' " in command:
                query=command.split(" l'")[1].strip()
            elif " e " in command:
                query=command.split(" e")[1].strip()
            elif " sara' " in command:
                query=command.split(" sara'")[1].strip()
            elif " sara " in command:
                query=command.split(" sara")[1].strip()
            elif " era " in command:
                query=command.split(" era")[1].strip()
            elif " al " in command:
                query=command.split(" al")[1].strip()
            elif " all " in command:
                query=command.split(" al")[1].strip()
            else:
                query=command.split(" e'")[1].strip()
            return query
        except IndexError:
            return "ERROR"

    def recov_preset_date(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        pattern = "%d-%m-%Y"
        if command == "che giorno e" or command == "che giorno e'":
            today_date  = datetime.datetime.now().date()
            formatted_date = today_date.strftime(pattern)
            return formatted_date
        if ("dopo" in command) and ("domani" in command):
            today = datetime.datetime.today()
            after_tomorrow = today + datetime.timedelta(days=2)
            formatted_date = after_tomorrow.strftime(pattern)
            return formatted_date
        if "domani" in command:
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            formatted_date = tomorrow.strftime(pattern)
            return formatted_date
        if "ieri" in command:
            today = datetime.datetime.today()
            yesterday = today + datetime.timedelta(days=-1)
            formatted_date = yesterday.strftime(pattern)
            return formatted_date
        if "oggi" in command:
            today = datetime.datetime.today()
            today = today + datetime.timedelta(days=0)
            formatted_date = today.strftime(pattern)
            return formatted_date
        return None

    def get_date(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        preset_date  = self.recov_preset_date(command)
        if preset_date is None:
            command_splitted = self.split_command(command)
            date = self.recov_date(command_splitted)
            output = self.gen_phrase(date)
            return output
        output = self.gen_phrase(preset_date)
        return output

    def get_diff(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        date  = self.recov_preset_date(command)
        if date is None:
            command_splitted = self.split_command(command)
            date = self.recov_date(command_splitted)
        day,month,year = date.split("-")
        day,month = self.clear_number(day,month)
        correct_date = datetime.datetime(int(year), int(month), int(day))
        diff_days = (datetime.datetime.now() - correct_date).days
        print(self.logger.log(
            f"result: Al {day} {month} {year} mancano {diff_days * -1}"),
              flush=True)
        if diff_days * -1 == 1:
            return f" Al {self.utils.number_to_word(day)} {self.utils.number_to_word(month)} {self.utils.number_to_word(year)} manca un giorno"
        return f" Al {self.utils.number_to_word(day)}, {self.utils.number_to_word(month)}, {self.utils.number_to_word(year)} mancano {self.utils.number_to_word(diff_days * -1)} giorni"
