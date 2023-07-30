from lib.prefix import Log
import webbrowser as web
import requests

# ---- This file is for search music and video via yt ----


def getTopic(command:str):
    try:
        if("play" in command):
            topic = command.split("play ")[1]
        if("riproduci" in command):
            topic = command.split("riproduci ")[1]
        print(Log(f" sto per riprodurre: {topic}"),flush=True)
        return topic
    except:
        print(Log(f" non ho capito il topic mi dispiace"),flush=True)
        #AUDIO ERROR



def playonyt(command: str) -> str:
        topic = getTopic(command)
        if(topic != None):
            url = f"https://www.youtube.com/results?q={topic}"
            count = 0
            cont = requests.get(url)
            data = cont.content
            data = str(data)
            lst = data.split('"')
            for i in lst:
                count += 1
                if i == "WEB_PAGE_TYPE_WATCH":
                    break
            if lst[count - 5] == "/results":
                raise Exception("No Video Found for this Topic!")
            web.open(f"https://www.youtube.com{lst[count - 5]}")
            return f"https://www.youtube.com{lst[count - 5]}"
    
