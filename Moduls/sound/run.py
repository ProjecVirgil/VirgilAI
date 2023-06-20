import gtts
import pygame
import os


current_path = os.getcwd()
file_path = os.path.join(current_path,'audio.mp3')

def create(text:str):
    pygame.mixer.music.unload()
    sound = gtts.gTTS(text,lang="it")
    sound.save(file_path)
    file = os.path.join(current_path, "audio.mp3")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
   
    return
    
    
    
    
