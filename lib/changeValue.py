import pygame 
import os

from lib.prefix import Log
from lib.sound import create
from lib.time import countNumber
current_path = os.getcwd()
file_path = os.path.join(current_path,'/asset')

# ---- File for change the volume of Virgil ----




def change(command:str):
    print(Log(" volume function"), flush=True)
    commandSplitted=command.split(" ")
    volume = commandSplitted[-1]
        
    if(countNumber(volume) >= 1):
        if( "%" in volume):
            volume = volume[:-1]
    else:
        print(Log("Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"), flush=True)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(f'{file_path}/ErrorValueVirgil.mp3 ')
    try:
        volume = int(volume)/100
        if(volume < 0.1 or volume > 1.0 ):
            return "104"
        else:
            return str(volume)
    except ValueError:
        print(Log("Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"), flush=True)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(f'{file_path}/ErrorValueVirgil.mp3 ')
        return "104"
    

    
    
    
