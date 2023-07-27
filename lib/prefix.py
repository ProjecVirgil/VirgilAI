from colorama import Fore,Back
import inspect
import time


def Log(string: str, filepath: str = None):
    callstack = inspect.stack()[1]
    caller = inspect.getmodule(callstack[0])
    prfx = (Fore.GREEN + f"(in module {caller})".format(caller) + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE)
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
