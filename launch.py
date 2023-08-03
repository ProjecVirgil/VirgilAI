import threading
import time
import string as st
import subprocess
import random
import os
import platform
import json

import pyfiglet
from colorama import Fore,Style

from lib.request import MakeRequests
from lib.logger import Logger   
from lib.output import Output
from lib.textInput import TextInput
from lib.vocalInput import VocalInput
from lib.procces import Process

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


    
def checkSystem():
    if SYSTEM == 'Windows':
                return "cls"
    elif SYSTEM == 'Darwin' or SYSTEM == 'Linux':
                # Esecuzione su macOS
                return "clear"
    else:
        print(logger.Log(WARNIGN + " Sistema operativo non riconosciuto. Impossibile avviare il terminale corrispondente.", flush=True))

def stampa(commandCleanear:str):
    delay = 0.1
    counter = 0
    for i in BANNER_MESSAGE:
        subprocess.run(commandCleanear, shell=True)
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
    
def rainbow(commandCleanear:str):
    delay = 0.1
    colori = [Fore.RED,Fore.YELLOW,Fore.GREEN,Fore.MAGENTA,Fore.CYAN,Fore.WHITE]
    for i in range(16):
        subprocess.run(commandCleanear, shell=True)
        print(Style.BRIGHT +  random.choice(colori)  + pyfiglet.figlet_format(BANNER_MESSAGE[-1]),flush=True)
        time.sleep(delay)
    subprocess.run(commandCleanear, shell=True)
    print(Style.BRIGHT +  Fore.MAGENTA  + pyfiglet.figlet_format(BANNER_MESSAGE[-1]),flush=True)
    print(Style.RESET_ALL,flush=True)

def installLibraries():
    print(logger.Log(string=ALERT +"START CHECK THE LIBRARY"),flush=True)
    command = "pip install -q -r setup/requirements.txt > logpip.txt"
    subprocess.run(command, shell=True)
    print(logger.Log(OK +"LIBRARY INSTALLED CORRECTLY IN CASE OF PROBLEMS, CHECK THE logpip.txt FILE"),flush=True)


def createAccount():
    print(logger.Log(OK + "I am creating your synchronization key"),flush=True)
    key = request_maker.createUser()
    request_maker.createUserEvent(key)
    print(logger.Log(OK + f"KEY {Fore.RED + str(key) + OK} CREATED CORRECTLY IN setup/key.txt "),flush=True)
    with open(KEY_FILE,'w') as fileKey:
        fileKey.write(str(key))
    check = input(logger.Log(ALERT + 'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '))
    print(logger.Log(OK + "Synchronizing your account settings"),flush=True)
    user = request_maker.getUser(key)
    with open(SETTINGS_FILE,'w') as f:
        json.dump(user,f,indent=4)
    if(user == 'User not found'):
        print(logger.Log(WARNIGN + "User not found"),flush=True)
        print(logger.Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),flush=True)
        exit(1)
    return key
        
def logIn():
    with open(KEY_FILE,'r') as fileKey:
        print(logger.Log(OK + "I pick up the key for synchronization"),flush=True)
        key = fileKey.readline()
        print(logger.Log(OK + "Synchronizing your account settings"),flush=True)
        user = request_maker.getUser(key)
    with open(SETTINGS_FILE,'w') as f:
        json.dump(user,f,indent=4)
    if(user == 'User not found'):
        print(logger.Log(WARNIGN + "User not found"),flush=True)
        print(logger.Log(ALERT + "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),flush=True)
        exit(1)
    return key
            
if __name__ == '__main__': 
#*  INIT LOGGER AND REQUEST_MAKER
    logger = Logger()
    request_maker = MakeRequests()
    
    #* CONST 
    BANNER_MESSAGE = ['W','We','Wel','Welc','Welco','Welcom','Welcome','Welcome ','Welcome t','Welcome to','Welcome to ','Welcome to V','Welcome to Vi','Welcome to Vir','Welcome to Virg','Welcome to Virgi','Welcome to Virgil']
    SYSTEM = platform.system()
    SETTINGS_FILE = "setup/settings.json"
    KEY_FILE = "setup/key.txt"
    ALERT = Style.BRIGHT + Fore.YELLOW
    OK = Style.BRIGHT + Fore.CYAN
    WARNIGN = Style.BRIGHT + Fore.RED
    
    
    commandCleaner = checkSystem()
    stampa(commandCleaner)
    rainbow(commandCleaner)
    installLibraries()

    if(os.path.getsize(KEY_FILE) == 0):
        key = createAccount()
    else:
        key = logIn()
        
#*  INIT ALL PRINCIPLE CLASS

    output = Output()
    process = Process()
    text_input = TextInput()
    vocal_input = VocalInput()
    
    
    print(logger.Log(OK + f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE"), flush=True)
    
    
    validChoise = False
    while(not validChoise):
        TextOrSpeech = str(input(logger.Log((ALERT + "You want a text interface (T) or recognise interface(R) T/R: ")))).upper()
        if(TextOrSpeech == 'T'):
            thread_1 = threading.Thread(target=text_input.text)
            thread_2 = threading.Thread(target=process.main)
            thread_3 = threading.Thread(target=output.out)
            validChoise = True
        elif(TextOrSpeech == 'R'):
            # Creazione di tre oggetti thread
            thread_1 = threading.Thread(target=vocal_input.speech)
            thread_2 = threading.Thread(target=process.main)
            thread_3 = threading.Thread(target=output.out)
            validChoise = True
        else:
            print(logger.Log(WARNIGN + " Select a valid choice please"),flush=True)
    
    print(logger.Log(OK +"PROGRAM IN EXECUTION"), flush=True)
    print("\n")
    print(logger.Log(OK + " THE PROGRAMMES WILL START SOON"),flush=True)
    thread_1.start()
    print(logger.Log(ALERT + " INPUT THREAD START..."),flush=True)
    thread_2.start()
    print(logger.Log(ALERT + " PROCESS THREAD START..."),flush=True)
    thread_3.start()
    print(logger.Log(ALERT + " OUTPUT THREAD START..."),flush=True)