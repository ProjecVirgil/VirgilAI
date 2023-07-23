from colorama import Fore,Back
import time

#Creation Templete for LOG:  
'''prfx=(Fore.GREEN + time.strftime ("%H:%M:%S UTC LOG", time.localtime() )+ Back.RESET + Fore.WHITE)
prfx = (prfx + " | ")'''

def Log(string:str):
    prfx=(Fore.GREEN + time.strftime ("%H:%M:%S UTC LOG", time.localtime() )+ Back.RESET + Fore.WHITE)
    prfx = (prfx + " | ")
    log = prfx + string
    return log

