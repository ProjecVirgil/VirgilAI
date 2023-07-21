import gtts
import pygame
import os
import json

current_path = os.getcwd()
file_path = os.path.join(current_path,'audio.mp3')


#Open file whith key api openai
with open(current_path + '/setting.json') as f:
    setting = json.load(f)
    volume = setting['volume']

def create(text:str):
    pygame.mixer.music.unload()
    if(pygame.mixer.music.get_volume != int(volume)):
        pygame.mixer.music.set_volume(int(volume))
    sound = gtts.gTTS(text,lang="it")
    sound.save(file_path)
    file = os.path.join(current_path, "audio.mp3")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    return
    
    
    
    