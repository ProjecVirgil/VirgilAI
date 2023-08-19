"""_summary_

    Returns:
        _type_: _description_
"""
import inspect
import time

import platform
from colorama import Fore,Back

# ---- This file make the preset for Log ----

class Logger:
    """_summary_
    """
    def __init__(self):
        self.current_call_stack = ''
        self.last_caller = ''
        self.__update_call_stack()

    def check_system(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        system = platform.system()
        if system == 'Windows':
            return "win"
        return "lin"

    def __update_call_stack(self):
        """_summary_
        """
        system = self.check_system()
        if system == "win":
            self.current_call_stack = inspect.stack()[2]
            self.last_caller = str(inspect.getmodule(self.current_call_stack[0])).split("\\")[-1]
        else:
            self.current_call_stack = inspect.stack()[2]
            self.last_caller = str(inspect.getmodule(self.current_call_stack[0])).split("\\")[-1]
            self.last_caller = self.last_caller.split("from")[1].split("/")[-1]

    def log(self, string: str, filepath: str = None):
        """_summary_

        Args:
            string (str): _description_
            filepath (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
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
