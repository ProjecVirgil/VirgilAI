"""File to manage the volume of Virgil."""
from lib.packages_utility.logger import logging
from lib.packages_utility.sound import Audio
from lib.packages_utility.utils import Utils

class VolumeMixer:
    """Class to control the sound volume of Virgil."""
    def __init__(self,volume_value:int = 100,settings = None):
        """Init file for class."""
        self.__volume = volume_value
        self.audio = Audio(settings.volume,settings.elevenlabs,settings.language)
        self.utils  = Utils()

    def get_volume(self) -> float or int:
        """Get current value from audio mixer.

        Returns:
            float/int: Volume
        """
        return self.__volume

    def change(self, command:str) -> str:
        """Change the volume of Virgil.

        Args:
            command (str): The input sentence

        Returns:
            str: Final message after change the volume
        """
        if self.utils.count_number(command) >= 1:
            def search_volume(command):
                return [x for x in command if x.isdigit()]
            self.__volume = int(search_volume(command)[0])
        else:
            logging.error("Sorry there was an error request the command with an appropriate value"),
            self.audio.create(file=True,namefile="ErrorValueVirgil")
            return "104"
        try:
            self.__volume = int(self.__volume)/100
            if self.__volume < 0.1 or self.__volume > 1.0 :
                return "104"
            return str(self.__volume)
        except ValueError:
            logging.error("Sorry there was an error request the command with an appropriate value"),
            self.audio.create(file=True,namefile="ErrorValueVirgil")
            return "104"
