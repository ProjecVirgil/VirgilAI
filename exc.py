import json
import time
import threading
from pyttsx3 import *




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
    engine.say("IL TIMER è FINITO")
    engine.runAndWait()
    #parte allarme
    
class TimerThread(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.daemon = True

    def run(self):
           timer(self.interval) 
           
if __name__ == "__main__":
    #init e setup the tts
    engine = init("sapi5")
    engine.setProperty("rate",180)
    voices = engine.getProperty("voices")
    engine.setProperty("voice",voices[0].id)
    voices=engine.getProperty("voices")
    
    engine.say("Sono Dante come posso aiutarti")
    engine.runAndWait()
    while(True):
        try:
            with open("main/res.json", 'r') as file:
                data = json.load(file)
                res = data["0"][1]
                command = data["0"][0]
                boole = data["0"][2]
            if(res != None and boole == False):
                if("volume" in command):
                        engine.setProperty('volume', res)
                        engine.say("bbbiiipp")
                        engine.runAndWait()
                        print(Log(f" volume cambiato correttamente a {res*100}% "))
                        update_json_value(2, True)
                elif("timer" in command):
                        print(f"Il timer è partito ci vediamo tra {res} secondi")
                        engine.say(f"Il timer è partito ci vediamo tra {res} secondi")
                        engine.runAndWait()
                        t = TimerThread(res)
                        t.start()
                        update_json_value(2, True)
                else:
                        engine.say(res)
                        engine.runAndWait()
                        print(res)
                        update_json_value(2, True)
            else:
                pass
        except json.decoder.JSONDecodeError:
            print(Log("Non è stato trovato niente nel json"))
            pass