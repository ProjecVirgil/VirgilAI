import random

from requests_html import HTMLSession
from lib.logger import Logger

# ---- This file generate a random news by GoogleNews ----




class Newsletter:
        
    def __init__(self) -> None:
        self.URL_RANDOM  = "https://news.google.com/rss?oc=5&hl=it&gl=IT&ceid=IT:it"
        self.logger = Logger()
        pass
    
    def getTopic(self,command:str):
        print(self.logger.Log(" specify topic"), flush=True)
        if(" di " in command):
            topic=command.split(" di ")[1]
            topic = topic.split(" ")[0]
        elif(" su " in command):
            topic=command.split(" su ")[1]
            topic = topic.split(" ")[0]
        elif(" sulle " in command):
            topic=command.split(" sulle ")[1]
            topic = topic.split(" ")[0]
        else:
            return None
        print(self.logger.Log(f" topic scelto: {topic}"), flush=True)
        return topic

            
    def createNews(self,command:str):
        print(self.logger.Log(" news function"), flush=True)
        s=HTMLSession()
        print(self.logger.Log(" session created"), flush=True)
        news= []
        topic = self.getTopic(command)
        
        if(topic != None):
            urlWithTopic = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
            r=s.get(urlWithTopic) 
            for title in r.html.find('title'):
                news.append(title.text)
            newsSelected = random.choice(news)
            print(self.logger.Log(f" news scelta {newsSelected}"), flush=True)
            return newsSelected
        else:
            print(self.logger.Log(" general topic"), flush=True)
            r=s.get(self.URL_RANDOM)
            for title in r.html.find('title'):
                news.append(title.text)
            newsSelected = random.choice(news)
            print(self.logger.Log(f" news scelta {newsSelected}"), flush=True)
            return newsSelected
    