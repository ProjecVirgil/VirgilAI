import gtts
import pygame
import os
import json
from elevenlabs import generate,save

current_path = os.getcwd()
file_path = os.path.join(current_path,'audio.mp3')


#Open file whith key api openai
with open(current_path + '/setting.json') as f:
    setting = json.load(f)
    volume = setting['volume']
    api_key = setting['elevenlabs']



def create(text:str):
    pygame.mixer.music.unload()
    if(pygame.mixer.music.get_volume != float(volume)):
        pygame.mixer.music.set_volume(float(volume))
    try:
        sound = generate(
            api_key = api_key,
            text=text,
            voice="Antoni",
            model='eleven_multilingual_v1'
        )
        save(sound,'audio.mp3')    
    except:
        sound = gtts.gTTS(text,lang="it")
        sound.save(file_path)

    file = os.path.join(current_path, "audio.mp3")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    return
    
    
    
    