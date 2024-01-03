"""Search a song on yt and reproduce it."""
import requests
import yt_dlp
from pygame.mixer import music

from lib.packages_utility.logger import logging


# ---- This file is for search music and video via yt ----

def search_on_yt(topic: str) -> str | None:
    """Search a song/video on youtube.

    Args:
        topic (str): the topic for the search

    Raises:
        Exception: Not video found

    Returns:
        str: The link for download
    """
    if topic != "None":
        url = f"https://www.youtube.com/results?q={topic}"
        count = 0
        cont = requests.get(url, timeout=10)
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


class MediaPlayer:
    """This class will be used to play media files.

    This class will be used to play media files.like audio,
    video or playlist in the background using pygme mixer library.
    """

    def __init__(self, synonymous: list) -> None:
        """Init the class and the logger class.

        Args:
            synonymous (list): a list of synonymous
        """
        self.synonymous = synonymous

    def get_topic(self, command: str) -> str or None:
        """Get the topic for search on yt.

        Args:
            command (str): sentence

        Returns:
            str: topic
        """
        topic = ""
        for word in self.synonymous:
            if word in command:
                topic = " ".join(command).split(word)[1]
                break
        if topic == "":
            topic = None
        return topic

    def download(self, url: str):
        """Download the audio from Youtube.

        Args:
            url (str): The url for the download
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
            try:
                error_code = ydl.download(url)
                return error_code
            except Exception as e:
                logging.error(f"Oh no it seems that ffmpeg is not installed, Install it from this link [https://ffmpeg.org/download.html] and try again - Error : {e}")
                return None

    def play(self):
        """Play the music file."""
        file_name = "music.wav"
        player_audio = music
        player_audio.unload()
        player_audio.load(file_name)
        player_audio.play()

    def play_music(self, command):
        """Play Music based on command.

        Args:
            command (str): the input sentence
        """
        topic = self.get_topic(command)
        logging.debug(f" topic selected: {topic}")
        url = search_on_yt(topic)
        logging.debug(f" url generated: {url}")
        self.download(url)
        self.play()
