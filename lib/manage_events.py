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
        except:
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
            command_splitted = self.calendar.split_command(command)
            date = self.calendar.recov_date(command_splitted)
            try:
                day,month,year = date.split("-")
            except:
                day,month,year = date.split(" ")
            day,month = self.calendar.clear_number(day,month)
            date = "-".join([day,month,year])
            return date
        return preset_date

    def add_events(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" i will create event"),flush=True)
        date,event = command.split("ho")
        if "che" in command:
            date_splited = date.split(" che ")[1]
            date = self.get_date(date_splited)
        elif "per" in command:
            date_splited = date.split(" per ")[1]
            date = self.get_date(date_splited)
        print(self.logger.log(" i recov the date"),flush=True)
        print(self.logger.log(" send the request"),flush=True)
        self.request_maker.create_events(event,date)
        return "Promemoria creato con successo"
