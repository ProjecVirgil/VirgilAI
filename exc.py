import json
import time
import threading
import os
import sys

import pygame
import gtts

from Moduls.sound import run
from prefix.creation import Log
from Moduls.CalendarRec import Recoverycalendar
from  Moduls.timeConv import TimeConversion




def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("main/res.json", 'r') as file:
        data = json.load(file)

    # Modifica il valore desiderato
    data["0"][key] = new_value

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("main/res.json", 'w') as file:
        json.dump(data, file, indent=4)



def timer(my_time):
    print(Log(" timer function"))
    print(Log(" inizio timer"))
    time.sleep(my_time)
    print(Log(" fine timer"))
    run.create(f"Timer finito")
    pygame.mixer.music.play()
    #parte allarme
    
class TimerThread(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.daemon = True

    def run(self):
           timer(self.interval) 
   

     
    
            
if __name__ == "__main__":
    pygame.init()
    #init e setup the tts
    run.create("Ciao sono virgilio come posso aiutarti?")
    time.sleep(3)
    while(True):
        try:
            with open("main/res.json", 'r') as file:
                data = json.load(file)
                res = data["0"][1]
                command = data["0"][0]
                bool = data["0"][2]
            if(res != None and bool == False):
                if("spento" in res):
                    print(Log(" shutdown in progress..."))
                    sys.exit(0)
                if("volume" in command):
                        pygame.mixer.music.set_volume(float(res))
                        run.create("biiip")
                        print(Log(f" volume changed correctly to {res*100}% "))
                        update_json_value(2, True)
                elif("timer" in command):
                        print(Log(f" the timer is started see you in {res} second"))
                        run.create(f" the timer is started see you in {res} second")
                        t = TimerThread(int(res))
                        t.start()
                        update_json_value(2, True)
                else:   
                        run.create(res)
                        print(res)
                        update_json_value(2, True)
            else:
                pass
            sys.stdout.flush()
        except json.decoder.JSONDecodeError:
            print(Log("Nothing was found in the json"))
            pass