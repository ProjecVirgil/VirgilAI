import json
import time
import threading
import sys

from colorama import Style,Fore
import pyfiglet
from pygame.mixer import music

from lib.sound import Audio
from lib.logger import Logger
from lib.utils  import Utils
from lib.manageEvents import EventScheduler


class Output:
    
    def __init__(self) -> None:
        self.event_scheduler = EventScheduler()
        self.logger = Logger()
        self.utils = Utils()
        self.audio = Audio()
        music.init()


    def update_json_value(self,key, new_value):
        # Apri il file JSON e carica i dati
        with open("connect/res.json", 'r') as file:
            data = json.load(file)

        # Modifica il valore desiderato
        data["0"][key] = new_value

        # Sovrascrivi il file JSON con i dati aggiornati
        with open("connect/res.json", 'w') as file:
            json.dump(data, file, indent=4)
            

    def checkReminder(self,):
        with open("connect/reminder.txt","r") as f:
            if(f.read() == "0"):
                with open("connect/reminder.txt","w") as f:
                    f.write("1")
                return False
            else:
                return True


    def timer(self, my_time, command):
        if "sveglia" in command:
            print(self.logger.Log(" timer function"), flush=True)
            print(self.logger.Log(" alarm clock actived"), flush=True)
            time.sleep(my_time)
            # AGGIUNGI QUI LA LOGICA DELL'ALARME
        else:
            print(self.logger.Log(" timer function"), flush=True)
            print(self.logger.Log(" start timer"), flush=True)
            time.sleep(my_time)
            print(self.logger.Log(" end timer"), flush=True)
            self.audio.create(file=True, namefile="timerEndVirgil")
        
    class TimerThread(threading.Thread):
        def __init__(self, interval, command):
            threading.Thread.__init__(self)
            self.interval = interval
            self.daemon = True
            self.command = command

        def run(self):
            output_instance = Output()
            output_instance.timer(self.interval, self.command)
    
    
    def recoverData(self,):
        with open("connect/res.json", 'r') as file:
            data = json.load(file)
            res = data["0"][1]
            command = data["0"][0]
            bool = data["0"][2]
            return res,command,bool

    def shutdown(self):
        print(self.logger.Log(" shutdown in progress..."), flush=True)
        self.audio.create(file=True,namefile="FinishVirgil")
        print(Style.BRIGHT +Fore.MAGENTA + pyfiglet.figlet_format("Thanks for using Virgil", font = "digital",justify= "center", width = 110 ), flush=True)
        print(Fore.LIGHTMAGENTA_EX + " - credit: @retr0", flush=True)
        print(Style.RESET_ALL, flush=True)
        time.sleep(2)
        sys.exit(0)

    def out(self,):
        self.audio.create(file=True,namefile="EntryVirgil")
        time.sleep(5)
        while(True):
            try:
                res,command,bool = self.recoverData()
                if(res != None and bool == False):
                    if("spento" in res):
                        self.shutdown()
                    if("volume" in command):
                        
                            music.set_volume(float(res))
                            music.unload()    
                            music.load('asset/bipEffectCheckSound.mp3')
                            music.play()       
                            print(self.logger.Log(f" volume changed correctly to {res*100}% "), flush=True)
                    
                    elif("timer" in command or "sveglia" in command):
                        
                            print(self.logger.Log(f" the timer is started see you in {res} second"), flush=True)
                            if("timer" in command):
                                self.audio.create(f"Il timer è partito ci vediamo tra {self.utils.numberToWord(res)} secondi")
                            else:
                                self.audio.create(f"Ho impostato la sveglia") #DA METTERRE COME PRESET
                            t = self.TimerThread(int(res),command)
                            t.start()
                            
                    else:   
                            self.audio.create(res)
                            print(res, flush=True)
                            
                    self.update_json_value(2, True)
                    
                    print(self.logger.Log(" check the reminder"),flush=True)
                    if(not self.checkReminder()):
                        print(self.logger.Log(" send notify for today event"),flush=True)
                        result = self.event_scheduler.sendNotify()
                        time.sleep(10)
                        self.audio.create(result)
                else:
                    pass
            except json.decoder.JSONDecodeError:
                print(self.logger.Log("Nothing was found in the json"), flush=True)
                pass
