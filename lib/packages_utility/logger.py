""""""

import inspect
import time
import json

import platform
from colorama import Fore,Back

# ---- This file make the preset for Log ----

class Logger:
    """
    This class is used to log all messages in a specific format.
    """
    def __init__(self):
        self.current_call_stack = ''
        self.last_caller = ''
        self.__update_call_stack()
        with open("setup/settings.json",encoding="utf8") as file:
            settings = json.load(file)
        self.lang = settings["language"]

    def check_system(self) -> str:
        """
        This function checks if you are using Windows or Linux and returns it's name.

        Returns:
            str: Windows or Linux
        """
        system = platform.system()
        if system == 'Windows':
            return "win"
        return "lin"

    def __update_call_stack(self) -> None:
        """
        This method updates call stack of current caller (function that called this one).
        """
        system = self.check_system()
        if system == "win":
            self.current_call_stack = inspect.stack()[2]
            self.last_caller = str(inspect.getmodule(self.current_call_stack[0])).split("\\")[-1]
        else:
            self.current_call_stack = inspect.stack()[2]
            self.last_caller = str(inspect.getmodule(self.current_call_stack[0])).split("\\")[-1]
            self.last_caller = self.last_caller.split("from")[1].split("/")[-1]

    def log(self, string: str, filepath: str = None) -> str:
        """
        This function logs message into console and saves it inside .log files.

        Args:
            string (str): The string to insert in the log message
            filepath (str, optional): File path for save the log Defaults to None.

        Returns:
            str: Return the log formatted
        """
        self.__update_call_stack()
        prfx = Fore.GREEN + f"(in module {self.last_caller[:-2]}) " + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE

        prfx = prfx + " | "
        log = prfx + string
        if filepath is not None:
            try:
                with open(filepath, "w",encoding="utf8") as file:
                    file.write(log)
                return ''
            except IOError:
                return log
        return log
