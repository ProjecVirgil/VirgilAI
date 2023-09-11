"""
File for the configuration of the other classes
"""
import json


class Settings:
    """
    Settings class for the application. This is a singleton object that holds all of our settings and can be accessed anywhere in the app through this single instance
    """
    def __init__(self) -> None:
        
    #******************** Setting ********************

        with open("setup/settings.json",encoding="utf8") as file:  
            settings = json.load(file)
            self.language = settings["language"]
            self.word_activation = settings["wordActivation"].lower()
            self.volume = settings["volume"]
            self.city = settings["city"]
            self.operation_timeout = settings["operation_timeout"]
            self.dynamic_energy_threshold = settings["dynamic_energy_threshold"]
            self.energy_threshold = settings["energy_threshold"]
            self.elevenlabs = settings["elevenlabs"]
            self.openai = settings["openAI"]
            self.merros_email = settings["merrosEmail"]
            self.merros_password = settings["merrosPassword"]
            self.temperature = settings["temperature"]
            self.max_tokens = settings["max_tokens"]

    #******************** Script language ********************

        with open(f'lang/{self.language}/{self.language}.json',encoding="utf8") as file:
            self.script = json.load(file)

            # ----- Calendar -----
            self.script_calendar = self.script["calendar"]
            self.phrase_calendar = self.script_calendar["phrase"]
            self.split_calendar = self.script_calendar["split"]
            self.months_calendar = self.script_calendar["month"]
            self.week_calendar = self.script_calendar["week"]
            self.words_meaning_tomorrow = self.script_calendar["words_meaning_tomorrow"]
            self.words_meaning_after_tomorrow = self.script_calendar["words_meaning_after_tomorrow"]
            self.words_meaning_yesterday = self.script_calendar["words_meaning_yesterday"]
            self.words_meaning_today = self.script_calendar["words_meaning_today"]
            # ----- Choose command -----

            self.script_command = self.script["command"]
            self.split_command = self.script_command["split"]

            # ----- Time -----
            self.scritp_time = self.script["time"]
            self.phrase_time = self.scritp_time["phrase"]
            self.split_time = self.scritp_time["split"]

            # ----- Process -----
            self.script_process = self.script["process"]
            self.prompt = self.script_process["prompt"]

            # ----- Events -----

            self.script_process = self.script["events"]
            self.phrase_events = self.script_process["phrase"]

            # ----- Outputs -----

            self.script_output = self.script["outputs"]
            self.phrase_output = self.script_output["phrase"]
            self.split_output = self.script_output["split"]

            # ----- News -----

            self.script_news = self.script["news"]
            self.sinonimi_news = self.script_news["sinonimi"]

            # ----- Wheather -----

            self.script_wheather = self.script["wheather"]
            self.phrase_wheather = self.script_wheather["phrase"]
            self.split_wheather = self.script_wheather["split"]
            self.wwc_wheather = self.script_wheather["WWC"]
            self.word_meaning_tomorrow_wheather = self.script_wheather["word_meaning_tomorrow"]

            # ----- Time -----

            self.scritp_time = self.script["time"]
            self.phrase_time = self.scritp_time["phrase"]
            self.split_time = self.scritp_time["split"]
