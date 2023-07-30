import datetime
import json
import time
import threading
import os
import sys

import pygame

from lib.sound import create
from lib.prefix import Log
from lib.numberConvertToText  import numberToWord
from lib.manageEvents import sendNotify


# ----- File to manage the result and hunt it as TTS -----

def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("connect/res.json", 'r') as file:
        data = json.load(file)

    # Modifica il valore desiderato
    data["0"][key] = new_value

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("connect/res.json", 'w') as file:
        json.dump(data, file, indent=4)
        

def checkReminder():
    with open("connect/reminder.txt","r") as f:
        if(f.read() == "0"):
            with open("connect/reminder.txt","w") as f:
                f.write("1")
            return False
        else:
            return True
    
    
def timer(my_time,command):
    if("sveglia" in command):
        print(Log(" timer function"), flush=True)
        print(Log(" alarm clock actived"), flush=True)
        time.sleep(my_time)
        #ADD ALARM CLOCK
    else:
        print(Log(" timer function"), flush=True)
        print(Log(" start timer"), flush=True)
        time.sleep(my_time)
        print(Log(" end timer"), flush=True)
        pygame.mixer.music.unload()    
        pygame.mixer.music.load('asset/timerEndVirgil.mp3') 
        pygame.mixer.music.play()       
    #parte allarme
class TimerThread(threading.Thread):
    def __init__(self, interval,command:str):
        threading.Thread.__init__(self)
        self.interval = interval
        self.daemon = True
        self.command = command

    def run(self):
           timer(self.interval,self.command) 
   

def recoverData():
    with open("connect/res.json", 'r') as file:
        data = json.load(file)
        res = data["0"][1]
        command = data["0"][0]
        bool = data["0"][2]
        return res,command,bool
    
    
if __name__ == "__main__":
    pygame.init()
    #init e setup the tts
    pygame.mixer.music.unload()    
    pygame.mixer.music.load('asset/EntryVirgil.mp3')   
    pygame.mixer.music.play()

    time.sleep(3)
    while(True):
        try:
            res,command,bool = recoverData()
            if(res != None and bool == False):
                if("spento" in res):
                    print(Log(" shutdown in progress..."), flush=True)
                    pygame.mixer.music.unload()    
                    pygame.mixer.music.load('asset/FinishVirgil.mp3') 
                    pygame.mixer.music.play()                  
                    time.sleep(2)
                    sys.exit(0)
                if("volume" in command):
                        pygame.mixer.music.set_volume(float(res))
                        pygame.mixer.music.unload()    
                        pygame.mixer.music.load('asset/bipEffectCheckSound.mp3')
                        pygame.mixer.music.play()       
                        print(Log(f" volume changed correctly to {res*100}% "), flush=True)
                        update_json_value(2, True)
                elif("timer" in command or "sveglia" in command):
                        print(Log(f" the timer is started see you in {res} second"), flush=True)
                        if("timer" in command):
                            create(f"Il timer è partito ci vediamo tra {numberToWord(res)} secondi")
                        else:
                            create(f"Ho impostato la sveglia") #DA METTERRE COME PRESET
                        t = TimerThread(int(res),command)
                        t.start()
                        update_json_value(2, True)
                else:   
                        create(res)
                        print(res, flush=True)
                        update_json_value(2, True)
                        
                #Cotrollo bit
                print(Log(" check the reminder"),flush=True)
                if(not checkReminder()):
                    print(Log(" send notify for today event"),flush=True)
                    result = sendNotify()
                    time.sleep(10)
                    create(result)
            else:
                pass
        except json.decoder.JSONDecodeError:
            print(Log("Nothing was found in the json"), flush=True)
            pass