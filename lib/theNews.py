import random

from requests_html import HTMLSession
from lib.prefix import Log
urlGen  = "https://news.google.com/rss?oc=5&hl=it&gl=IT&ceid=IT:it"

urlSpec = "https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"


def createNews(command:str):
    print(Log(" news function"))
    s=HTMLSession()
    print(Log(" session created"))
    News= []
    if(" di " in command):
        print(Log(" specify topic"))
        topic=command.split(" di ")[1]
        topic = topic.split(" ")[0]
        print(Log(f" topic scelto: {topic}"))
        urlSpec = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
        r=s.get(urlSpec) 
        for title in r.html.find('title'):
            News.append(title.text)
        news = random.choice(News)
        print(Log(f" news scelta {news}"))
        return news 
    elif(" su " in command):
        print(Log(" specify topic"))
        topic=command.split(" su ")[1]
        topic = topic.split(" ")[0]
        print(Log(f" topic scelto: {topic}"))
        urlSpec = f"https://news.google.com/rss/search?q={topic}&hl=it&gl=IT&ceid=IT:it"
        r=s.get(urlSpec) 
        for title in r.html.find('title'):
            News.append(title.text)
        news = random.choice(News)
        print(Log(f" news scelta {news}"))
        return news 
    else:
        print(Log(" general topic"))
        r=s.get(urlGen)
        for title in r.html.find('title'):
            News.append(title.text)
        news = random.choice(News)
        print(Log(f" news scelta {news}"))
        return news
   