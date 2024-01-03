"""File to format and send events to DB."""
import datetime

from lib.packages_utility.logger import logging
from lib.packages_utility.request import MakeRequests
from lib.packages_secondary.calendar_rec import Calendar, clear_number


# ----- Calendar Event Function -----
class EventScheduler:
    """This class is used to schedule calendar events for the user using the VirgilAPI and DB."""

    def __init__(self, settings):
        """Init the class."""
        self.request_maker = MakeRequests()
        self.calendar = Calendar(settings)

        self.lang = settings.language
        self.settings = settings
        self.phrase_events = settings.phrase_events

        self.events = self.request_maker.get_events(self.settings.key_user)
        self.current_date = datetime.datetime.now().date()
        self.formatted_date = self.current_date.strftime("%d-%m-%Y")
        self.formatted_date = self.formatted_date.split("-")
        self.formatted_date[1] = self.formatted_date[1].replace("0", "")
        self.formatted_date = "-".join(self.formatted_date)



    def send_notify(self) -> str:
        """This function sends a notification.

        This function sends a notification to the users that have an
        event on today's date, if they are not already notified about it.

        Returns:
            str: The phrase to reproduce
        """
        try:
            today_events = self.events[self.formatted_date]
            phrase = self.phrase_events[0]
            for event in today_events:
                phrase = phrase + event.strip() + " "
        except KeyError:
            phrase = self.phrase_events[1]
        logging.info(f" {phrase}")
        return phrase

    def get_date(self, command) -> str:
        """This function gets a date from the command line.

        Args:
            command (_type_): Sentence

        Returns:
            str: The date recovered
        """
        preset_date = self.calendar.recov_preset_date(command)
        if preset_date is None:
            date = self.calendar.recover_date(command)
            try:
                day, month, year = date.split("-")
            except ValueError:
                day, month, year = date.split(" ")
            day, month = clear_number(day, month)
            date = "-".join([day, month, year])
            return date
        return preset_date

    def recognize_date(self, command) -> tuple:
        """Take the data and the event for send the request.

        Args:
            command (_type_): Sentence

        Returns:
            tuple: Date for the events and the event
        """
        words = self.settings.words_meaning_after_tomorrow + self.settings.words_meaning_tomorrow + self.settings.words_meaning_yesterday + self.settings.words_meaning_today

        for word in words:
            if word in command:
                with open("connect/command.json", encoding="utf8") as commands:
                    command_complete = commands.read()
                    event = "".join("".join(command_complete.split(word)[1]).split('":'))[:-7]
                return word.split(" "), event

        date_record = []
        for element in command:
            if element.isdigit() or element in self.settings.months_calendar:
                date_record.append(element)
                if len(date_record) >= 3:  # noqa: PLR2004
                    break
        event = " ".join(command).split(date_record[-1])
        return date_record, event

    def add_events(self, command: str) -> str:
        """Add an event to a specific date.

        Args:
            command (str): sentence input

        Returns:
            str: Final phrase to reproduce
        """
        date, event = self.recognize_date(command)
        date = self.get_date(date)
        self.request_maker.create_events(event, date,self.settings,self.settings.key_user)
        return self.phrase_events[2]
