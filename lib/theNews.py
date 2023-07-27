import random

from requests_html import HTMLSession
from lib.prefix import Log

urlGenRandom  = "https://news.google.com/rss?oc=5&hl=it&gl=IT&ceid=IT:it"
urlSpec = "https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"


def createNews(command:str):
    print(Log(" news function"))
    s=HTMLSession()
    print(Log(" session created"))
    news= []
    
    if(" di " in command):
        print(Log(" specify topic"))
        topic=command.split(" di ")[1]
        topic = topic.split(" ")[0]
        print(Log(f" topic scelto: {topic}"))
        urlWithTopic = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
        r=s.get(urlWithTopic) 
        for title in r.html.find('title'):
            news.append(title.text)
        newsSelected = random.choice(news)
        print(Log(f" news scelta {newsSelected}"))
        return newsSelected
    
    elif(" su " in command):
        print(Log(" specify topic"))
        topic=command.split(" su ")[1]
        topic = topic.split(" ")[0]
        #return topic
        print(Log(f" topic scelto: {topic}"))
        urlWithTopic = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
        r=s.get(urlWithTopic) 
        for title in r.html.find('title'):
            news.append(title.text)
        newsSelected = random.choice(news)
        print(Log(f" news scelta {newsSelected}"))
        return newsSelected
    else:
        #return "no topic"
        print(Log(" general topic"))
        r=s.get(urlGenRandom)
        for title in r.html.find('title'):
            news.append(title.text)
        newsSelected = random.choice(news)
        print(Log(f" news scelta {newsSelected}"))
        return newsSelected
   