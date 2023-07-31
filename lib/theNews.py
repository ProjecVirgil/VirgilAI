import random

from requests_html import HTMLSession
from lib.prefix import Log

# ---- This file generate a random news by GoogleNews ----




class Newsletter:
        
    def __init__(self) -> None:
        self.URL_RANDOM  = "https://news.google.com/rss?oc=5&hl=it&gl=IT&ceid=IT:it"
        pass
    
    def getTopic(self,command:str):
        if(" di " in command):
            print(Log(" specify topic"), flush=True)
            topic=command.split(" di ")[1]
            topic = topic.split(" ")[0]
            print(Log(f" topic scelto: {topic}"))
            return topic
        elif(" su " in command):
            print(Log(" specify topic"), flush=True)
            topic=command.split(" su ")[1]
            topic = topic.split(" ")[0]
            #return topic
            print(Log(f" topic scelto: {topic}"), flush=True)
            return topic
        elif(" sulle " in command):
            print(Log(" specify topic"), flush=True)
            topic=command.split(" sulle ")[1]
            topic = topic.split(" ")[0]
            #return topic
            print(Log(f" topic scelto: {topic}"), flush=True)
            return topic
        else:
            return None
            
    def createNews(self,command:str):
        print(Log(" news function"), flush=True)
        s=HTMLSession()
        print(Log(" session created"), flush=True)
        news= []
        topic = self.getTopic(command)
        
        if(topic != None):
            urlWithTopic = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
            r=s.get(urlWithTopic) 
            for title in r.html.find('title'):
                news.append(title.text)
            newsSelected = random.choice(news)
            print(Log(f" news scelta {newsSelected}"), flush=True)
            return newsSelected
        else:
            print(Log(" general topic"), flush=True)
            r=s.get(self.URL_RANDOM)
            for title in r.html.find('title'):
                news.append(title.text)
            newsSelected = random.choice(news)
            print(Log(f" news scelta {newsSelected}"), flush=True)
            return newsSelected
    