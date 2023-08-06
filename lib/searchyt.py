import requests
import yt_dlp
from pygame.mixer import music

from lib.logger import Logger
# ---- This file is for search music and video via yt ----



class MediaPlayer:
    def __init__(self) -> None:
        self.logger  = Logger()
        
    def getTopic(self,command:str):
        try:
            if("play" in command):
                topic = command.split("play ")[1]
            if("riproduci" in command):
                topic = command.split("riproduci ")[1]
            return topic
        except:
            pass
            #AUDIO ERROR


    #MODIFICARE TO GET ONLY URL 
    def searchOnYt(seld,topic:str) -> str:
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
                return f"https://www.youtube.com{lst[count - 5]}"
            

    def download(self,URL):
        nameFile = "music"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': nameFile + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(URL)
            
    def play(self):
        filename = "music.wav"
        #pygame.mixer.init()
        playerAudio = music
        playerAudio.unload()
        playerAudio.load(filename)
        playerAudio.play()
            
            
    def playMusic(self,command):
        topic = self.getTopic(command)
        print(self.logger.Log(f" topic selected: {topic}"),flush=True)
        URL = self.searchOnYt(topic)
        print(self.logger.Log(f" url gererater: {URL}"),flush=True)
        self.download(URL)
        self.play()
        
