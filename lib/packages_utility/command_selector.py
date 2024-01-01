"""CommandSelector is a class that selects and executes the appropriate command based on user input."""
from lib.packages_secondary.time import Time, diff_time
from lib.packages_secondary.the_weather import Weather
from lib.packages_secondary.the_news import Newsletter
from lib.packages_secondary.searchyt import MediaPlayer
from lib.packages_secondary.llm_models import LLModel

from lib.packages_utility.logger import logging

class CommandSelector:
    """This class is responsible for selecting and executing the appropriate command based on user input."""
    def __init__(self,settings,class_manager) -> None:
        """Initializes a new instance of the `CommandSelector` class.

        Args:
            settings (_type_): _description_
            class_manager (_type_): _description_
        """
        self.utils = class_manager.utils
        self.audio = class_manager.audio
        self.event_scheduler = class_manager.event_scheduler
        self.calendar = class_manager.calendar

        self.time = Time(settings.language,settings.split_time,settings.phrase_time,self.utils)
        self.weather = Weather(settings,self.audio,self.utils)
        self.news_letter = Newsletter(settings.language, settings.synonyms_news)
        self.media_player = MediaPlayer(settings.synonyms_mediaplayer)
        self.LLM = LLModel(openai_key=settings.openai,language=settings.language,gpt_version=settings.gpt_version,max_tokens=settings.max_tokens,prompt=settings.prompt)


    def get_time(self,_) -> str:
        """Executes the time related commands.

        Args:
            _ (_type_): not used

        Returns:
            str: The actual time
        """
        return self.time.now()

    def change_volume(self,input:list[str]) -> str:
        """Changes the volume level of the audio output device.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The audio code response
        """
        response = self.audio.change(input)
        if response == "104":
            print("\nVirgil: You cannot give a value less than 10, you can only give values from 100 to 10",
                        flush=True)
            self.audio.create(file=True, namefile="ErrorValueVolume")
            return None
        return response

    def get_weather(self,input:list[str]) -> str:
        """Gets and returns the weather information for the city specified in the user's request. If no city is provided it will use the default one.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The phrase formatted with the weather information
        """
        return self.weather.recover_weather(input)

    def get_timer(self,input:list[str]) -> str:
        """Execute timer related commands.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The duration of timer in seconds
        """
        for i in input:
            if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                hours, minutes, calculated_hours, calculated_minutes, calculate_seconds = diff_time(i)
                time_calculated = f"{calculated_hours} hours {calculated_minutes} minutes {calculate_seconds} seconds".split(
                            " ")
                my_time = self.time.conversion(list(time_calculated))
                return str(my_time)
        try:
            my_time = self.time.conversion(input)
            return str(my_time)
        except IndexError:
                logging.error("Please try the command again")
                self.audio.create(file=True, namefile="GenericError")
                return

    def get_date(self,input:list[str]) -> str:
        """Execute date related commands.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The phrase formatted with the relative date information
        """
        return self.calendar.get_date(input)

    def get_mc(self,input:list[str]) -> str:
        """Execute some function related to day.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The phrase formatted with the relative day information
        """
        for i in input:
            if self.utils.count_number(i) >= 2:  # noqa: PLR2004
                hours, minutes, calculated_hours, calculated_minutes, calculate_seconds = diff_time(i)
                logging.info(
                    f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minutes)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.utils.number_to_word(calculated_minutes)} {self.utils.number_to_word(calculate_seconds)}")
                return f" {self.settings.split_time[1]} {self.utils.number_to_word(hours)} {self.settings.split_time[3]} {self.utils.number_to_word(minutes)} {self.settings.phrase_time[6]} {self.utils.number_to_word(calculated_hours)} {self.settings.phrase_time[1]} {self.utils.number_to_word(calculated_minutes)} {self.settings.phrase_time[2]} {self.utils.number_to_word(calculate_seconds)} {self.settings.phrase_time[3]}"
        return self.calendar.diff_date(input)

    def get_news(self,input:list[str]) -> str:
        """Execute news related commands.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: The phrase formatted with the relative news information
        """
        return self.news_letter.create_news(input)

    def play_music(self,input:list[str]) -> None:
        """Play music from youtube.

        Args:
            input (list[str]): The command cleaned
        """
        self.media_player.play_music(input)

    def add_events(self,input:list[str]) -> str:
        """Add events on calendar.

        Args:
            input (list[str]): The command cleaned

        Returns:
            str: A simple phrase to reproduce for the success of command
        """
        return self.event_scheduler.add_events(input)

    def generate_response(self,input:str) -> str:
        """Generate a response based on user's input.

        Args:
            input (str): The command not cleaned

        Returns:
            str: The response of LLM model
        """
        result = self.LLM.gen_response("".join(input))
        logging.info(f"Generated response: {result}")
        return result
