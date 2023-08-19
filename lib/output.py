"""_summary_

    Returns:
        _type_: _description_
"""
import json
import time
import threading
import sys

from colorama import Style,Fore
import pyfiglet
from pygame import mixer

from lib.sound import Audio
from lib.logger import Logger
from lib.utils  import Utils
from lib.manage_events import EventScheduler


class Output:
    """_summary_
    """
    def __init__(self) -> None:
        self.event_scheduler = EventScheduler()
        self.logger = Logger()
        self.utils = Utils()
        self.audio = Audio()
        mixer.init()


    def update_json_value(self,key, new_value):
        """_summary_

        Args:
            key (_type_): _description_
            new_value (_type_): _description_
        """
        # Apri il file JSON e carica i dati
        with open("connect/res.json", 'r',encoding="utf8") as file:
            data = json.load(file)

        # Modifica il valore desiderato
        data["0"][key] = new_value

        # Sovrascrivi il file JSON con i dati aggiornati
        with open("connect/res.json", 'w',encoding="utf8") as file:
            json.dump(data, file, indent=4)

    def check_reminder(self,):
        """_summary_

        Returns:
            _type_: _description_
        """
        with open("connect/reminder.txt","r",encoding="utf8") as file:
            if file.read() == "0":
                with open("connect/reminder.txt","w",encoding="utf8") as file:
                    file.write("1")
                return False
            return True


    def timer(self, my_time, command):
        """_summary_

        Args:
            my_time (_type_): _description_
            command (_type_): _description_
        """
        if "sveglia" in command:
            print(self.logger.log(" timer function"), flush=True)
            print(self.logger.log(" alarm clock actived"), flush=True)
            time.sleep(my_time)
            # AGGIUNGI QUI LA LOGICA DELL'ALARME
        else:
            print(self.logger.log(" timer function"), flush=True)
            print(self.logger.log(" start timer"), flush=True)
            time.sleep(my_time)
            print(self.logger.log(" end timer"), flush=True)
            self.audio.create(file=True, namefile="timerEndVirgil")

    class TimerThread(threading.Thread):
        """_summary_

        Args:
            threading (_type_): _description_
        """
        def __init__(self, interval, command):
            threading.Thread.__init__(self)
            self.interval = interval
            self.daemon = True
            self.command = command

        def run(self):
            """_summary_
            """
            output_instance = Output()
            output_instance.timer(self.interval, self.command)

    def recover_data(self,):
        """_summary_

        Returns:
            _type_: _description_
        """
        with open("connect/res.json", 'r',encoding="utf8") as file:
            data = json.load(file)
            res = data["0"][1]
            command = data["0"][0]
            is_used = data["0"][2]
            return res,command,is_used

    def shutdown(self):
        """_summary_
        """
        print(self.logger.log(" shutdown in progress..."), flush=True)
        self.audio.create(file=True,namefile="FinishVirgil")
        print(Style.BRIGHT +Fore.MAGENTA + pyfiglet.figlet_format("Thanks for using Virgil",
                                                                  font = "digital",
                                                                  justify= "center",
                                                                  width = 110 ),
            flush=True)
        print(Fore.LIGHTMAGENTA_EX + " - credit: @retr0", flush=True)
        print(Style.RESET_ALL, flush=True)
        time.sleep(2)
        sys.exit(0)

    def out(self):
        """_summary_
        """
        self.audio.create(file=True,namefile="EntryVirgil")
        time.sleep(5)
        while True:
            try:
                result,command,is_used = self.recover_data()
                if result != None and is_used is False:
                    if "spento" in result:
                        self.shutdown()
                    if "volume" in command:
                        mixer.music.set_volume(float(result))
                        mixer.music.unload()
                        mixer.music.load('asset/bipEffectCheckSound.mp3')
                        mixer.music.play()
                        print(self.logger.log(f" volume changed correctly to {result*100}% "),
                              flush=True)

                    elif "timer" in command or "sveglia" in command:
                        print(self.logger.log(f" the timer is started see you in {result} second"),
                              flush=True)
                        if "timer" in command:
                            self.audio.create(
                                f"Il timer è partito ci vediamo tra {self.utils.number_to_word(result)} secondi")
                        else:
                            self.audio.create(file=True,namefile="ClockImposter")
                        thread = self.TimerThread(int(result),command)
                        thread.start()
                    else:
                        self.audio.create(result)
                        print(result, flush=True)
                    self.update_json_value(2, True)

                    print(self.logger.log(" check the reminder"),flush=True)
                    if not self.check_reminder():
                        print(self.logger.log(" send notify for today event"),flush=True)
                        result = self.event_scheduler.send_notify()
                        time.sleep(10)
                        self.audio.create(result)
                else:
                    pass
            except json.decoder.JSONDecodeError:
                print(self.logger.log("Nothing was found in the json"), flush=True)
