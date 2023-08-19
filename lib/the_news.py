"""_summary_

    Returns:
        _type_: _description_
"""
import random

from requests_html import HTMLSession
from lib.logger import Logger

# ---- This file generate a random news by GoogleNews ----




class Newsletter:
    """_summary_
    """
    def __init__(self) -> None:
        self.url_random  = "https://news.google.com/rss?oc=5&hl=it&gl=IT&ceid=IT:it"
        self.logger = Logger()

    def get_topic(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" specify topic"), flush=True)
        if " di " in command:
            topic=command.split(" di ")[1]
            topic = topic.split(" ")[0]
        elif " su " in command:
            topic=command.split(" su ")[1]
            topic = topic.split(" ")[0]
        elif " sulle " in command:
            topic=command.split(" sulle ")[1]
            topic = topic.split(" ")[0]
        else:
            return None

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
    