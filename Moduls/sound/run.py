import gtts
import pygame
import os
def create(text:str):
    pygame.mixer.music.unload()
    sound = gtts.gTTS(text,lang="it")
    sound.save("F:/ProjectVirgilio/audio.mp3")
    file = os.path.join("F:/ProjectVirgilio", "audio.mp3")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
   
    
    return
    
    
    
    
