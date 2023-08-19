"""_summary_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
"""
import requests
import yt_dlp
from pygame.mixer import music

from lib.logger import Logger
# ---- This file is for search music and video via yt ----

class MediaPlayer:
    """_summary_
    """
    def __init__(self) -> None:
        self.logger  = Logger()

    def get_topic(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            if "play" in command:
                topic = command.split("play ")[1]
            if "riproduci" in command:
                topic = command.split("riproduci ")[1]
            return topic
        except requests.RequestException:
            return "None"
            #AUDIO ERROR


    #MODIFICARE TO GET ONLY URL
    def search_on_yt(self,topic:str) -> str:
        """_summary_

        Args:
            seld (_type_): _description_
            topic (str): _description_

        Raises:
            Exception: _description_

        Returns:
            str: _description_
        """
        if topic != "None":
            url = f"https://www.youtube.com/results?q={topic}"
            count = 0
            cont = requests.get(url,timeout=10)
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
        return None

    def download(self,url):
        """_summary_

        Args:
            URL (_type_): _description_
        """
        name_file = "music"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': name_file + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)
            return error_code

    def play(self):
        """_summary_
        """
        file_name = "music.wav"
        player_audio = music
        player_audio.unload()
        player_audio.load(file_name)
        player_audio.play()


    def play_music(self,command):
        """_summary_

        Args:
            command (_type_): _description_
        """
        topic = self.get_topic(command)
        print(self.logger.log(f" topic selected: {topic}"),flush=True)
        url = self.search_on_yt(topic)
        print(self.logger.log(f" url gererater: {url}"),flush=True)
        self.download(url)
        self.play()
