"""
    summary: The start file
"""
import sys
import threading
import time
import subprocess
import random
import os
import platform
import json

import pyfiglet
from colorama import Fore,Style

from lib.word2vec import GloVeVectorizer,sentence_to_vec
from lib.request import MakeRequests
from lib.logger import Logger
from lib.output import Output
from lib.text_input import TextInput
from lib.vocal_input import VocalInput
from lib.procces import Process

# ---- This file launch all the file for making Virgilio work  ----
def check_system():
    """
    Check if system is windows or linux and return a string with it's name clear command

    Returns:
        str or int: If the system is recognize return a correct command for the OS 
    """
    if SYSTEM == 'Windows':
        return "cls"
    if SYSTEM in ('Darwin', 'Linux'):
        # Esecuzione su macOS
        return "clear"
    print(
        logger.log(
            WARNIGN + " Sistema operativo non riconosciuto.Impossibile avviare il terminale corrispondente."),
            flush=True
            )
    return 404

def print_banner(command_cleaner:str):
    """
    Print the main banner of Virgil

    Args:
        COMMAND_CLEANER (str): The command for clear the console
    """
    delay = 0.1
    counter = 0
    for i in BANNER_MESSAGE:
        subprocess.run(command_cleaner, shell=True,check=False)
        print(Style.BRIGHT+ Fore.MAGENTA + pyfiglet.figlet_format(i),flush=True)
        if counter == 11:
            delay  = 0.2
        elif counter == 12:
            delay  = 0.25
        elif counter == 13:
            delay  = 0.3
        elif counter == 14:
            delay  = 0.35
        elif counter == 15:
            delay  = 0.4
        time.sleep(delay)
        counter+=1
    print(Style.RESET_ALL,flush=True)

def rainbow(command_cleanear:str):
    """
    Animation rainbow on the first banner

    Args:
        commandCleanear (str): The command for clear the console
    """
    delay = 0.1
    colori = [Fore.RED,Fore.YELLOW,Fore.GREEN,Fore.MAGENTA,Fore.CYAN,Fore.WHITE]
    for _ in range(16):
        subprocess.run(command_cleanear,shell=True,check=False)
        print(
        Style.BRIGHT +
        random.choice(colori) +
        pyfiglet.figlet_format(BANNER_MESSAGE[-1]),flush=True
        )
        time.sleep(delay)
    subprocess.run(command_cleanear, shell=True,check=False)
    print(Style.BRIGHT +  Fore.MAGENTA  + pyfiglet.figlet_format(BANNER_MESSAGE[-1]),flush=True)
    print(Style.RESET_ALL,flush=True)

def install_libraries():
    """
    Install and check all libraries needed by virgil
    """
    print(logger.log(string=ALERT +"START CHECK THE LIBRARY"),flush=True)
    command = "pip install -q -r setup/requirements.txt > logpip.txt"
    subprocess.run(command, shell=True,check=False)
    print(
        logger.log(
            OK +"LIBRARY INSTALLED CORRECTLY IN CASE OF PROBLEMS, CHECK THE logpip.txt FILE"),
            flush=True
        )


def create_account() -> str:
    """
    Create a new account with Virgil API

    Returns:
        str: return the key of account created
    """
    print(logger.log(OK + "I am creating your synchronization key"),flush=True)
    key = request_maker.create_user()
    request_maker.create_user_event(key)

    print(logger.log(OK + f"KEY {Fore.RED + str(key) + OK} CREATED CORRECTLY IN setup/key.txt "),
          flush=True
          )

    with open(KEY_FILE,'w',encoding="utf8") as file_key:
        file_key.write(str(key))
    _ = input(logger.log(
        ALERT +
        'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '))
    print(logger.log(OK + "Synchronizing your account settings"),flush=True)
    user = request_maker.get_user_settings(key)

    with open(SETTINGS_FILE,'w',encoding="utf8") as file:
        json.dump(user,file,indent=4)

    if user == 'User not found':
        print(logger.log(WARNIGN + "User not found"),flush=True)
        print(logger.log(
            ALERT +
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),
                flush=True)
        sys.exit(1)
    return key

def log_in() -> str:
    """
    Log in to an existing account using its private key saved on disk (setup/key.txt).

    Returns:
        str: return the key of account created
    """
    with open(KEY_FILE,'r',encoding="utf8") as file_key:
        print(logger.log(OK + "I pick up the key for synchronization"),flush=True)
        key = file_key.readline()
        print(logger.log(OK + "Synchronizing your account settings"),flush=True)
        user = request_maker.get_user_settings(key)
    with open(SETTINGS_FILE,'w',encoding="utf8") as file:
        json.dump(user,file,indent=4)
    if user == 'User not found' :
        print(logger.log(WARNIGN + "User not found"),flush=True)
        print(logger.log(
            ALERT +
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),
            flush=True)
        sys.exit(1)
    return key

def main():
    """

    Main function that will be called when running this script from command line
    
    """
    command_cleaner = check_system()
    print_banner(command_cleaner)
    rainbow(command_cleaner)
    install_libraries()

    if os.path.getsize(KEY_FILE) == 0:
        key = create_account()
    else:
        key = log_in()

    if not os.path.exists("model/model_en.pkl"):  
        print(logger.log(ALERT + " Start the download of english model this operation will take some time, but will only be done once "))
        request_maker.download_model_en()
        print(logger.log(OK + " Download finish"))
    
#*  INIT ALL PRINCIPLE CLASS
    output = Output()
    process = Process()
    text_input = TextInput()
    vocal_input = VocalInput()


    print(logger.log(OK + f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE"), flush=True)

    thread_1 = 0
    thread_2 = 0
    thread_3 = 0

    valid_choise = False
    while not valid_choise:
        text_or_speech = str(input(
            logger.log(
                (ALERT + "You want a text interface (T) or recognise interface(R) T/R: ")
                ))).upper()
        if text_or_speech == 'T':
            thread_1 = threading.Thread(target=text_input.text)
            thread_2 = threading.Thread(target=process.main)
            thread_3 = threading.Thread(target=output.out)
            valid_choise = True
        elif text_or_speech == 'R':
            # Creazione di tre oggetti thread
            thread_1 = threading.Thread(target=vocal_input.listening)
            thread_2 = threading.Thread(target=process.main)
            thread_3 = threading.Thread(target=output.out)
            valid_choise = True
        else:
            print(logger.log(WARNIGN + " Select a valid choice please"),flush=True)

    print(logger.log(OK +"PROGRAM IN EXECUTION"), flush=True)
    print("\n",flush=True)
    print(logger.log(OK + " THE PROGRAMMES WILL START SOON"),flush=True)
    thread_1.start()
    print(logger.log(ALERT + " INPUT THREAD START..."),flush=True)
    thread_2.start()
    print(logger.log(ALERT + " PROCESS THREAD START..."),flush=True)
    thread_3.start()
    print(logger.log(ALERT + " OUTPUT THREAD START..."),flush=True)

if __name__ == '__main__':
     #*  INIT LOGGER AND REQUEST_MAKER
    logger = Logger()
    request_maker = MakeRequests()

    #* CONST
    BANNER_MESSAGE = ['W','We','Wel','Welc','Welco','Welcom','Welcome','Welcome ',
                      'Welcome t','Welcome to','Welcome to ','Welcome to V','Welcome to Vi',
                      'Welcome to Vir','Welcome to Virg','Welcome to Virgi','Welcome to Virgil']
    SYSTEM = platform.system()
    SETTINGS_FILE = "setup/settings.json"
    KEY_FILE = "setup/key.txt"
    ALERT = Style.BRIGHT + Fore.YELLOW
    OK = Style.BRIGHT + Fore.CYAN
    WARNIGN = Style.BRIGHT + Fore.RED

    main()
