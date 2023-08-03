import gtts
from pygame import mixer
import os
import json

from elevenlabs import generate,save

from lib.logger import Logger

# ---- This file make the TTS ----
class Audio:
    def __init__(self):
        self.logger = Logger()
        #Open file whith key api openai
        with open("setup/settings.json") as f:
            SETTINGS = json.load(f)
            self.volume = SETTINGS['volume']
            self.API_KEY = SETTINGS['elevenlabs']
        
    def create(self,text:str = "",file:bool = False,namefile:str = ""):
        mixer.music.unload()
        if(mixer.music.get_volume != float(self.volume)):
            mixer.music.set_volume(float(self.volume))
            
            if(file):
                file = os.path.join(f"asset/{namefile}.mp3")
                mixer.music.load(file)
                mixer.music.play()
                return
            else:
                try:
                    sound = generate(
                        api_key = self.API_KEY,
                        text=text,
                        voice="Antoni",
                        model='eleven_multilingual_v1'
                    )
                    save(sound,'audio.mp3')    
                except:
                    print(self.logger.Log(" Google text to speech has started the cause could be a missing valid key or the end of the elevenLabs plan if you are aware of this you can ignore the message"), flush=True)
                    sound = gtts.gTTS(text,lang="it")
                    sound.save("audio.mp3")

        file = os.path.join("audio.mp3")
        mixer.music.load(file)
        mixer.music.play()
        
        
        