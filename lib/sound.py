import gtts
import pygame
import os
import json

from elevenlabs import generate,save

from lib.logger import Logger

# ---- This file make the TTS ----



#Open file whith key api openai
with open("setting.json") as f:
    setting = json.load(f)
    volume = setting['volume']
    api_key = setting['elevenlabs']

class Audio:
    
    def __init__(self):
        self.logger = Logger()
        pass

    def create(self,text:str = "",file:bool = False,namefile:str = ""):
        pygame.mixer.music.unload()
        if(pygame.mixer.music.get_volume != float(volume)):
            pygame.mixer.music.set_volume(float(volume))
            
            if(file):
                file = os.path.join(f"asset/{namefile}.mp3")
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
                return
            else:
                try:
                    sound = generate(
                        api_key = api_key,
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
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        
        return
        
        
        