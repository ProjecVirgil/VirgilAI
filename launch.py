import time
import string as st
import subprocess
import random
import os
import platform
import json

import pyfiglet
from colorama import Fore,Style

from lib.request import createUser,getUser
from lib.prefix import Log

'''string = "Thanks for use Virgil"
print("[")
for i in range(len(string) + 1):
    print("'",end='')
    for x in range(i):
        print(string[x],end='')
    print("'",end='')
    print(",",end='')
print("]")'''

bannerMessage = ['W','We','Wel','Welc','Welco','Welcom','Welcome','Welcome ','Welcome t','Welcome to','Welcome to ','Welcome to V','Welcome to Vi','Welcome to Vir','Welcome to Virg','Welcome to Virgi','Welcome to Virgil']
system = platform.system()
if system == 'Windows':
            commandClean = "cls"
elif system == 'Darwin' or system == 'Linux':
            # Esecuzione su macOS
            commandClean = "clear"
else:
    print("Sistema operativo non riconosciuto. Impossibile avviare il terminale corrispondente.")

def stampa():
    global commandClean
    delay = 0.1
    c = 0
    for i in bannerMessage:
        subprocess.run(commandClean, shell=True)
        print(Style.BRIGHT+ Fore.MAGENTA + pyfiglet.figlet_format(i),flush=True)
        if(c == 11 ):
            delay  = 0.2
        elif(c == 12):
            delay  = 0.25
        if(c == 13 ):
            delay  = 0.3
        elif(c == 14):
            delay  = 0.35
        elif(c == 15):
            delay  = 0.4
        time.sleep(delay)
        c+=1
    print(Style.RESET_ALL,flush=True)
    
def rainbow():
    global commandClean
    delay = 0.1
    colori = [Fore.RED,Fore.YELLOW,Fore.GREEN,Fore.MAGENTA,Fore.CYAN,Fore.WHITE]
    for i in range(16):
        subprocess.run(commandClean, shell=True)
        print(Style.BRIGHT +  random.choice(colori)  + pyfiglet.figlet_format(bannerMessage[-1]),flush=True)
        time.sleep(delay)
    subprocess.run(commandClean, shell=True)
    print(Style.BRIGHT +  Fore.MAGENTA  + pyfiglet.figlet_format(bannerMessage[-1]),flush=True)
    print(Style.RESET_ALL,flush=True)

if __name__ == '__main__': 
    ALERT = Style.BRIGHT + Fore.YELLOW
    OK = Style.BRIGHT + Fore.CYAN
    WARNIGN = Style.BRIGHT + Fore.RED
    stampa()
    rainbow()
    print(Log(ALERT +"START CHECK THE LIBRARY"),flush=True)
    command = "pip install -q -r setupAndLaunch/requirements.txt > logpip.txt"
    subprocess.run(command, shell=True)
    print(Log(OK +"LIBRARY INSTALLED CORRECTLY IN CASE OF PROBLEMS, CHECK THE logpip.txt FILE"),flush=True)
    
    #TAKE KEY
    current_path = os.getcwd()
    current_path = current_path.replace("\ ".strip() , "/")
    
    if(os.path.getsize(f"{current_path}/setupAndLaunch/key.txt") == 0):
        print(Log(OK + "I am creating your synchronization key"))
        key = createUser()
        print(Log(OK + f"KEY CREATED CORRECTLY {current_path}/setupAndLaunch/key.txt "))
        with open(f"{current_path}/setupAndLaunch/key.txt",'w') as fileKey:
            fileKey.write(str(key))
        print(Log(OK + "Synchronizing your account settings"))
        user = getUser(key)
        with open(f"setting.json",'w') as f:
            json.dump(user,f,indent=4)
        if(user == 'User not found'):
            print(Log(WARNIGN + "User not found"))
            print(Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"))
            exit(1)

    else:
        with open(f"{current_path}/setupAndLaunch/key.txt",'r') as fileKey:
            print(Log(OK + "I pick up the key for synchronization"))
            key = fileKey.readline()
            print(Log(OK + "Synchronizing your account settings"))
            user = getUser(key)
        with open(f"setting.json",'w') as f:
            json.dump(user,f,indent=4)
        if(user == 'User not found'):
            print(Log(WARNIGN + "User not found"))
            print(Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"))
            exit(1)

            

    print(Log(OK + f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE"))
        
    Valid = False
    while(not Valid):
        TorS = str(input(Log((ALERT + "You want a text interface (T) or recognise interface(R) T/R: ")))).upper()
        if(TorS == 'T'):
            print(Log(OK +"STARTING THE PYTHON FILE"),flush=True)
            process = ["procces.py","output.py","textInput.py"]
            for proc in process:
                if system == 'Windows':
                    # Esecuzione su Windows
                    subprocess.Popen(['start', 'cmd', '/k', 'python', proc], shell=True)
                elif system == 'Darwin':
                    # Esecuzione su macOS
                    subprocess.Popen(['open', '-a', 'Terminal', 'python', proc], shell=True)
                elif system == 'Linux':
                    # Esecuzione su Linux (utilizzando GNOME Terminal) da FIXARE
                    subprocess.run('gnome-terminal -- python3 ' + proc,shell=True)                       
                else:
                    print(Log(WARNIGN + "Sistema operativo non riconosciuto. Impossibile avviare il terminale corrispondente."))
                Valid = True
        elif(TorS == 'R'):
            print(Log(OK +"STARTING THE PYTHON FILE"),flush=True)
            process = ["procces.py","output.py","vocalInput.py"]
            for proc in process:
                if system == 'Windows':
                    # Esecuzione su Windows
                    subprocess.Popen(['start', 'cmd', '/k', 'python', proc], shell=True)
                elif system == 'Darwin':
                    # Esecuzione su macOS
                    subprocess.Popen(['open', '-a', 'Terminal', 'python', proc], shell=True)
                elif system == 'Linux':
                    # Esecuzione su Linux (utilizzando GNOME Terminal) da FIXARE
                    subprocess.run('gnome-terminal -- python3 ' + proc,shell=True)                       
                else:
                    print(Log(WARNIGN + "Sistema operativo non riconosciuto. Impossibile avviare il terminale corrispondente."),flush=True)
                Valid = True
        else:
            print(Log(WARNIGN + "Select a valid choice please"),flush=True)
            
    print(Log(OK +"PROGRAM IN EXECUTION"), flush=True)
    print("\n")
    print(Style.BRIGHT +Fore.MAGENTA + pyfiglet.figlet_format("Thanks for using Virgil", font = "digital",justify= "center", width = 110 ))
    print(Fore.LIGHTMAGENTA_EX + " - credit: @retr0")
    print(Style.RESET_ALL)