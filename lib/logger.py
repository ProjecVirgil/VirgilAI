from colorama import Fore,Back

import inspect
import time

# ---- This file make the preset for Log ----

class Logger:
    def __init__(self):
        self.currentCallstack = ''
        self.lastCaller = ''
        self.__updateCallstack()

    def __updateCallstack(self):
        self.currentCallstack = inspect.stack()[2]
        self.lastCaller = str(inspect.getmodule(self.currentCallstack[0])).split("\\")[-1]

    def Log(self, string: str, filepath: str = None):
        self.__updateCallstack()
        prfx = (Fore.GREEN + f"(in module {self.lastCaller[:-2]}) " + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE)
        prfx = (prfx + " | ")
        log = prfx + string
        if filepath is not None:
            try:
                with open(filepath, "w") as f:
                    f.write(log)
                return ''
            except IOError:
                return log
        return log
