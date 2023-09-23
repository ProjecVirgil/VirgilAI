"""A file for manage and reproduce the last news by google news."""
import random

from requests_html import HTMLSession

from lib.packages_utility.logger import Logger

# ---- This file generate a random news by GoogleNews ----

class Newsletter:
    """This class is used to recover a news from google api."""
    def __init__(self,language,synonyms_news) -> None:
        """Init the language,logger class and some synonymus.

        Args:
            language (_type_): _description_
            synonyms_news (_type_): _description_
        """
        self.logger = Logger()

        self.lang = language
        self.url_random = f"https://news.google.com/rss?oc=5&hl={self.lang}&gl={self.lang.upper()}&ceid={self.lang.upper()}:{self.lang}"
        self.synonyms_news = synonyms_news

    def get_topic(self,command) -> None or str:
        """This function return the topic of the command received as parameter.

        Args:
            command (str): sentence

        Returns:
            str: The topic in the phrase
        """
        print(self.logger.log(" specify topic"), flush=True)
        topic = ""
        for word in self.synonyms_news:
            if word in command:
                topic = " ".join(command).split(word)[1]
                break
        if topic == "":
            topic = None
        print(self.logger.log(f" topic choised: {topic}"), flush=True)
        return topic

    def create_news(self,command:str) -> str:
        """This method will be called when you want to retrieve some news about something.

        Args:
            command (str): sentence input

        Returns:
            str: The news generated
        """
        session=HTMLSession()
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
            request=session.get(self.url_random)
            for title in request.html.find('title'):
                news.append(title.text)
            news_selected = random.choice(news)
            print(self.logger.log(f" news choise {news_selected}"), flush=True)

        return news_selected
