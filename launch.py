import time
import string as st
import subprocess
import random
import os
import platform
import json

import pyfiglet
from colorama import Fore,Style

from lib.request import createUser,getUser,createUserEvent
from lib.prefix import Log

# ---- This file launch all the file for making Virgilio work  ----


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
    counter = 0
    for i in bannerMessage:
        subprocess.run(commandClean, shell=True)
        print(Style.BRIGHT+ Fore.MAGENTA + pyfiglet.figlet_format(i),flush=True)
        if(counter == 11 ):
            delay  = 0.2
        elif(counter == 12):
            delay  = 0.25
        if(counter == 13 ):
            delay  = 0.3
        elif(counter == 14):
            delay  = 0.35
        elif(counter == 15):
            delay  = 0.4
        time.sleep(delay)
        counter+=1
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
    command = "pip install -q -r setup/requirements.txt > logpip.txt"
    subprocess.run(command, shell=True)
    print(Log(OK +"LIBRARY INSTALLED CORRECTLY IN CASE OF PROBLEMS, CHECK THE logpip.txt FILE"),flush=True)
    
    #TAKE KEY
    current_path = os.getcwd()
    current_path = current_path.replace("\ ".strip() , "/")
    
    if(os.path.getsize(f"{current_path}/setup/key.txt") == 0):
        print(Log(OK + "I am creating your synchronization key"),flush=True)
        key = createUser()
        createUserEvent(key)
        print(Log(OK + f"KEY {Fore.RED + str(key) + OK} CREATED CORRECTLY IN {current_path}/setup/key.txt "),flush=True)
        with open(f"{current_path}/setup/key.txt",'w') as fileKey:
            fileKey.write(str(key))
        check = input(Log(ALERT + 'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '),flush=True)
        print(Log(OK + "Synchronizing your account settings"),flush=True)
        user = getUser()
        with open(f"setting.json",'w') as f:
            json.dump(user,f,indent=4)
        if(user == 'User not found'):
            print(Log(WARNIGN + "User not found"),flush=True)
            print(Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),flush=True)
            exit(1)

    else:
        with open(f"{current_path}/setup/key.txt",'r') as fileKey:
            print(Log(OK + "I pick up the key for synchronization"),flush=True)
            key = fileKey.readline()
            print(Log(OK + "Synchronizing your account settings"),flush=True)
            user = getUser(key)
        with open(f"setting.json",'w') as f:
            json.dump(user,f,indent=4)
        if(user == 'User not found'):
            print(Log(WARNIGN + "User not found"),flush=True)
            print(Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),flush=True)
            exit(1)

            

    print(Log(OK + f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE"))
        
    Valid = False
    while(not Valid):
        TextOrSpeech = str(input(Log((ALERT + "You want a text interface (T) or recognise interface(R) T/R: ")))).upper()
        if(TextOrSpeech == 'T'):
            print(Log(OK +"STARTING THE PYTHON FILE"),flush=True)
            processes = ["procces.py","output.py","textInput.py"]
            for process in processes:
                if system == 'Windows':
                    # Esecuzione su Windows
                    subprocess.Popen(['start', 'cmd', '/k', 'python', process], shell=True)
                elif system == 'Darwin':
                    # Esecuzione su macOS
                    subprocess.Popen(['open', '-a', 'Terminal', 'python', process], shell=True)
                elif system == 'Linux':
                    # Esecuzione su Linux (utilizzando GNOME Terminal) da FIXARE
                    subprocess.run('gnome-terminal --  python3 ' + process,shell=True)                           
                else:
                    print(Log(WARNIGN + "Sistema operativo non riconosciuto. Impossibile avviare il terminale corrispondente."))
                Valid = True
        elif(TextOrSpeech == 'R'):
            print(Log(OK +"STARTING THE PYTHON FILE"),flush=True)
            processes = ["procces.py","output.py","vocalInput.py"]
            for process in processes:
                if system == 'Windows':
                    # Esecuzione su Windows
                    subprocess.Popen(['start', 'cmd', '/k', 'python', process], shell=True)
                elif system == 'Darwin':
                    # Esecuzione su macOS
                    subprocess.Popen(['open', '-a', 'Terminal', 'python', process], shell=True)
                elif system == 'Linux':
                    # Esecuzione su Linux (utilizzando GNOME Terminal) da FIXARE
                    subprocess.run('gnome-terminal -- python3 ' + process,shell=True)                       
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