"""
_summary_
"""
import os
import json

import gtts
from pygame.mixer import music
from elevenlabs import generate,save,api

from lib.logger import Logger

# ---- This file make the TTS ----
class Audio:
    """
    _summary_
    """
    def __init__(self):
        self.logger = Logger()
        #Open file whith key api openai
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
            self.volume = settings['volume']
            self.api_key = settings['elevenlabs']

    def create(self,text:str = "",file:bool = False,namefile:str = ""):
        """_summary_

        Args:
            text (str, optional): _description_. Defaults to "".
            file (bool, optional): _description_. Defaults to False.
            namefile (str, optional): _description_. Defaults to "".
        """
        music.unload()
        if music.get_volume != float(self.volume):
            music.set_volume(float(self.volume))
            if file:
                file = os.path.join(f"asset/{namefile}.mp3")
                music.load(file)
                music.play()
                return
            try:
                sound = generate(
                    api_key = self.api_key,
                    text=text,
                    voice="Antoni",
                    model='eleven_multilingual_v1'
                )
                save(sound,'audio.mp3')
            except api.error.APIError:
                print(self.logger.log(" Google text to speech has started the cause could be a missing valid key or the end of the elevenLabs plan if you are aware of this you can ignore the message"), flush=True)
                sound = gtts.gTTS(text,lang="it")
                sound.save("audio.mp3")

        file = os.path.join("audio.mp3")
        music.load(file)
        music.play()
