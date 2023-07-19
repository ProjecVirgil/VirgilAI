import json
import time
import threading
import os
import sys

import pygame

current_path = os.getcwd()
current_path = current_path.replace("\ ".strip() , "/")
sys.path.append(current_path + "/lib")


from lib.sound import create
from lib.prefix import Log




def update_json_value(key, new_value):
    # Apri il file JSON e carica i dati
    with open("connect/res.json", 'r') as file:
        data = json.load(file)

    # Modifica il valore desiderato
    data["0"][key] = new_value

    # Sovrascrivi il file JSON con i dati aggiornati
    with open("connect/res.json", 'w') as file:
        json.dump(data, file, indent=4)



def timer(my_time):
    print(Log(" timer function"), flush=True)
    print(Log(" inizio timer"), flush=True)
    time.sleep(my_time)
    print(Log(" fine timer"), flush=True)
    create(f"Timer finito")
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
    create("Ciao sono virgilio come posso aiutarti?")
    time.sleep(3)
    while(True):
        try:
            with open("connect/res.json", 'r') as file:
                data = json.load(file)
                res = data["0"][1]
                command = data["0"][0]
                bool = data["0"][2]
            if(res != None and bool == False):
                if("spento" in res):
                    print(Log(" shutdown in progress..."), flush=True)
                    create(" Spegnimento in corso...")
                    time.sleep(2)
                    sys.exit(0)
                if("volume" in command):
                        pygame.mixer.music.set_volume(float(res))
                        create("biiip")
                        print(Log(f" volume changed correctly to {res*100}% "), flush=True)
                        update_json_value(2, True)
                elif("timer" in command):
                        print(Log(f" the timer is started see you in {res} second"), flush=True)
                        create(f" Il timer è partito ci vediamo tra {res} second")
                        t = TimerThread(int(res))
                        t.start()
                        update_json_value(2, True)
                else:   
                        create(res)
                        print(res, flush=True)
                        update_json_value(2, True)
            else:
                pass
        except json.decoder.JSONDecodeError:
            print(Log("Nothing was found in the json"))
            pass