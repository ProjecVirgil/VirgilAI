"""_summary_

    Returns:
        _type_: _description_
"""
import json
import random

from requests_html import HTMLSession
from lib.logger import Logger

# ---- This file generate a random news by GoogleNews ----

class Newsletter:
    """_summary_
    """
    def __init__(self) -> None:
        self.logger = Logger()
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
            self.lang = settings["language"]

        self.url_random = f"https://news.google.com/rss?oc=5&hl={self.lang}&gl={self.lang.upper()}&ceid={self.lang.upper()}:{self.lang}"

        with open(f'lang/{self.lang}/{self.lang}.json',encoding="utf8") as file:
            self.script = json.load(file)
            self.scritp_time = self.script["news"]
            self.split = self.scritp_time["split"]

        #add to json
        self.sinonimi = [
            "novita","avvenimento","evento","aneddoto","fatto","informazione","cronaca",
            "comunicazione","segnalazione","rapporto","avvenimenti","eventi",
            "aneddoti","fatti","informazioni","cronache","comunicazioni","segnalazioni","rapporti",
            "notizie","notizia"]

    def get_topic(self,command):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" specify topic"), flush=True)
        topic = ""
        for word in self.sinonimi:
            if word in command:
                topic = " ".join(command).split(word)[1]
                break
        if topic == "":
            topic = None
        print(self.logger.log(f" topic scelto: {topic}"), flush=True)
        return topic

    def create_news(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" news function"), flush=True)
        session=HTMLSession()
        print(self.logger.log(" session created"), flush=True)
        news= []
        topic = self.get_topic(command)

        if topic is not None:
            url_with_topic = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
            request=session.get(url_with_topic)
            for title in request.html.find('title'):
                news.append(title.text)
            news_selected = random.choice(news)
            print(self.logger.log(f" news scelta {news_selected}"), flush=True)
        else:
            print(self.logger.log(" general topic"), flush=True)
            request=session.get(self.url_random)
            for title in request.html.find('title'):
                news.append(title.text)
            news_selected = random.choice(news)
            print(self.logger.log(f" news scelta {news_selected}"), flush=True)

        return news_selected
