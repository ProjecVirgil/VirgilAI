"""_summary_

    Returns:
        _type_: _description_
"""
from lib.logger import Logger
from lib.sound import Audio
from lib.utils import Utils

# ---- File for change the volume of Virgil ----


class VolumeMixer:
    """_summary_
    """
    def __init__(self, volume_value:int = 100):
        self.__volume = volume_value
        self.logger = Logger()
        self.audio = Audio()
        self.utils  = Utils()

    def get_volume(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__volume

    def change(self, command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        print(self.logger.log(" volume function"), flush=True)
        if self.utils.count_number(command) >= 1:
            search_volume = lambda command: [x for x in command if x.isdigit()]
            self.__volume = int(search_volume(command)[0])
        else:
            print(self.logger.log(
                "Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"),
                  flush=True)
            self.audio.create(file=True,namefile="ErrorValueVirgil")
            return "104"
        try:
            self.__volume = int(self.__volume)/100
            if self.__volume < 0.1 or self.__volume > 1.0 :
                return "104"
            return str(self.__volume)
        except ValueError:
            print(self.logger.log(
                "Mi dispiace c'è stato un errore richiedimi il comando con un valore adeguato"),
                  flush=True)
            self.audio.create(file=True,namefile="ErrorValueVirgil")
            return "104"
