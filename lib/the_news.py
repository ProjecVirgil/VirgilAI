""""""
import random

from requests_html import HTMLSession

from lib import Settings
from lib.logger import Logger

# ---- This file generate a random news by GoogleNews ----

class Newsletter:
    """
    This class is used to recover a news from google api.
    """
    def __init__(self) -> None:
        self.logger = Logger()
        self.settings = Settings()
        self.lang = self.settings.language
        self.url_random = f"https://news.google.com/rss?oc=5&hl={self.lang}&gl={self.lang.upper()}&ceid={self.lang.upper()}:{self.lang}"


    def get_topic(self,command) -> None or str:
        """
        This function return the topic of the command received as parameter

        Args:
            command (str): sentence

        Returns:
            str: The topic in the phrase
        """
        print(self.logger.log(" specify topic"), flush=True)
        topic = ""
        for word in self.settings.synonyms_news:
            if word in command:
                topic = " ".join(command).split(word)[1]
                break
        if topic == "":
            topic = None
        print(self.logger.log(f" topic choised: {topic}"), flush=True)
        return topic

    def create_news(self,command:str) -> str:
        """
        This method will be called when you want to retrieve some news about something.

        Args:
            command (str): sentence input

        Returns:
            str: The news generated
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
            print(self.logger.log(f" news choise {news_selected}"), flush=True)
        else:
            print(self.logger.log(" general topic"), flush=True)
            request=session.get(self.url_random)
            for title in request.html.find('title'):
                news.append(title.text)
            news_selected = random.choice(news)
            print(self.logger.log(f" news choise {news_selected}"), flush=True)

        return news_selected
