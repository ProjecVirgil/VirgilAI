"""_summary_

    Returns:
        _type_: _description_
"""
import datetime

from lib.logger import Logger
from lib.request import MakeRequests
from lib.calendar_rec import Calendar

# ----- Calendar Event Function -----
class EventScheduler:
    """_summary_
    """
    def __init__(self):
        self.logger = Logger()
        self.request_maker = MakeRequests()
        self.calendar = Calendar()

        self.events = self.request_maker.get_events()
        self.current_date = datetime.datetime.now().date()
        self.formatted_date = self.current_date.strftime("%d-%m-%Y")
        self.formatted_date = self.formatted_date.split("-")
        self.formatted_date[1] = self.formatted_date[1].replace("0", "")
        self.formatted_date = "-".join(self.formatted_date)

    def send_notify(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            today_events = self.events[self.formatted_date]
            phrase = "Ciao ti ricordo che oggi hai vari impegni: "
            for event in today_events:
                phrase = phrase + event.strip() + " "
        except ValueError:
            phrase = "Oggi non hai nessun impegno goditi la giornata"
        print(self.logger.log(f" {phrase}"), flush=True)
        return phrase


    def get_date(self,command):
        """_summary_

        Args:
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        preset_date  = self.calendar.recov_preset_date(command)
        if preset_date is None:
            date = self.calendar.recover_date(command)
            try:
                day,month,year = date.split("-")
            except ValueError:
                day,month,year = date.split(" ")
            day,month = self.calendar.clear_number(day,month)
            date = "-".join([day,month,year])
            return date
        return preset_date

    def recognize_date(self,command):
        """_summary_

        Args:
            command (_type_): _description_

        Returns:
            _type_: _description_
        """
        months = self.calendar.mesi_dell_anno
        words = self.calendar.parole_significato_domani + self.calendar.parole_significato_dopo_domani + self.calendar.parole_significato_ieri + self.calendar.parole_significato_oggi

        for word in words:
            if word in command:
                with open("connect/command.json", 'r',encoding="utf8") as commands:
                    command_complete = commands.read()
                    event = "".join("".join(command_complete.split(word)[1]).split('":'))[:-7]
                return word.split(" "),event

        date_record = []
        for element in command:
            if element.isdigit() or element in months:
                date_record.append(element)
                if len(date_record) >= 3:
                    break
        event = " ".join(command).split(date_record[-1])
        return date_record,event

    def add_events(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" i will create event"),flush=True)
        date,event = self.recognize_date(command)
        date = self.get_date(date)
        print(self.logger.log(" i recov the date"),flush=True)
        print(self.logger.log(" send the request"),flush=True)
        self.request_maker.create_events(event,date)
        return "Promemoria creato con successo"
