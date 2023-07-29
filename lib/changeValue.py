import pygame 
import os

from lib.prefix import Log
from lib.sound import create

current_path = os.getcwd()
file_path = os.path.join(current_path,'/asset')

# ---- File for change the volume of Virgil ----

def change(command:str):
    print(Log(" volume function"))
    commandSplitted=command.split(" ")
    volume = commandSplitted[-1]
    
    if("." in volume and "%" in volume): # 20%.  / 20.  /
        volume = volume[:-2]
    elif( "%" in volume or "." in volume):
        volume = volume[:-1]
    try:
        volume = int(volume)/100
        if(volume < 0.1 or volume > 1.0 ):
            return "104"
        else:
            return str(volume)
    except ValueError:
        print(Log("Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"))
        pygame.mixer.music.unload()
        pygame.mixer.music.load(f'{file_path}/ErrorValueVirgil.mp3 ')
        return "104"
    

    
    
    
