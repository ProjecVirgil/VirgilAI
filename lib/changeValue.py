import os
import json

from lib.prefix import Log
from lib.sound import create
from lib.time import countNumber

# ---- File for change the volume of Virgil ----


class VolumeMixer:
    #settings_path = f"{current_path}/setting.json"

    def __init__(self, sValue: int = 100):
        self.__volume = sValue
        self.current_path = os.getcwd()
        self.file_path = os.path.join(self.current_path, '/asset')

    def getVolume(self):
        return self.__volume

    def change(self, command:str):
        print(Log(" volume function"), flush=True)
        commandSplit = command.split(" ")
        self.__volume = commandSplit[-1]

        if(countNumber(self.__volume) >= 1):
            if( "%" in self.__volume):
                self.__volume = self.__volume[:-1]
        else:
            print(Log("Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"), flush=True)
            create(file=True,namefile="ErrorValueVirgil")
            return "104"


        try:
            self.__volume = int(self.__volume)/100
            if(self.__volume < 0.1 or self.__volume > 1.0 ):
                return "104"
            else:
                return str(self.__volume)
        except ValueError:
            print(Log("Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"), flush=True)
            create(file=True,namefile="ErrorValueVirgil")
            return "104"
