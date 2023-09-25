"""summary: The start file."""
import sys
import threading
import time
import subprocess
import random
import os
import platform
import json

import tomli
import pyfiglet
from colorama import Fore,Style

from lib.packages_utility.utils import init_settings
import lib.packages_utility.vectorize   # noqa: F401
from lib.packages_utility.request import MakeRequests
from lib.packages_utility.logger import Logger


# ---- This file launch all the file for making Virgilio work  ----
def check_system():
    """Check if system is windows or linux and return a string with it's name clear command.

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
            WARNIGN + " Unrecognized operating system.Unable to start the corresponding terminal"),
            flush=True
            )
    return 404

def print_banner(command_cleaner:str):
    """Print the main banner of Virgil.

    Args: COMMAND_CLEANER (str): The command for clear the console
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
    """Animation rainbow on the first banner.

    Args: commandCleanear (str): The command for clear the console
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
    print(Style.BRIGHT +  Fore.MAGENTA  + pyfiglet.figlet_format(BANNER_MESSAGE[-1]),
          flush=True)
    print(Style.RESET_ALL,flush=True)

def install_libraries():
    """Install and check all libraries needed by virgil.

    #TODO to change on a check update function
    """
    print(logger.log(string=ALERT +"START CHECK THE LIBRARY"),flush=True)


def create_account() -> str:
    """Create a new account with Virgil API.

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
    """Log in to an existing account using its private key saved on disk (setup/key.txt).

    Returns:
        str: return the key of account created
    """
    with open(KEY_FILE,encoding="utf8") as file_key:
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

def choise_input():
    """This function is used when you want to choose between the text input or Voice input.

    Returns:
        str: the type of input
    """
    while True:
        text_or_speech = str(input(
            logger.log(
                ALERT + "You want a text interface (T) or recognise interface(R) T/R: "
                ))).upper()
        if text_or_speech == 'T':
            return 1
        elif text_or_speech == 'R':
            # Creazione di tre oggetti thread
            return 0
        else:
            print(logger.log(WARNIGN + " Select a valid choice please"),flush=True)

def main():
    """Main function that will be called when running this script from command line."""
    from lib.packages_main.output import Output
    from lib.packages_main.text_input import TextInput
    from lib.packages_main.vocal_input import VocalInput
    from lib.packages_main.procces import Process

    command_cleaner = check_system()
    print_banner(command_cleaner)
    rainbow(command_cleaner)
    install_libraries()

    key = create_account() if (os.path.getsize(KEY_FILE)  == 0 ) or not os.path.exists(KEY_FILE) else log_in()

    if not os.path.exists("model/model_en.pkl"):
        print(logger.log(ALERT + " Start the download of english model this operation will take some time, but will only be done once "))
        request_maker.download_model_en()
        print(logger.log(OK + " Download finish"))


    #*INIT ALL PRINCIPLE CLASS
    output = Output(settings)
    process = Process(settings)
    text_input = TextInput(word_activation=settings.word_activation)
    vocal_input = VocalInput(settings)

    print(logger.log(OK + f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE"), flush=True)

    thread_1 = 0
    thread_2 = 0
    thread_3 = 0

    # IF THE DISPLAY IS FALSE NON MOSTRI QUESTO INPUT E PRENDI QUELLO DI DEFAULT
    if(defaul_start == 'N'):
        text_or_speech = choise_input()
        if text_or_speech == 1:
                thread_1 = threading.Thread(target=text_input.text)
                thread_2 = threading.Thread(target=process.main)
                thread_3 = threading.Thread(target=output.out)
        elif text_or_speech == 0:
                thread_1 = threading.Thread(target=vocal_input.listening)
                thread_2 = threading.Thread(target=process.main)
                thread_3 = threading.Thread(target=output.out)
        else:
                print(logger.log(WARNIGN + " Select a valid choice please"),flush=True)
    elif(defaul_start == 'T'):
         thread_1 = threading.Thread(target=text_input.text)
         thread_2 = threading.Thread(target=process.main)
         thread_3 = threading.Thread(target=output.out)
    else:
        thread_1 = threading.Thread(target=vocal_input.listening)
        thread_2 = threading.Thread(target=process.main)
        thread_3 = threading.Thread(target=output.out)

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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    toml_path = 'pyproject.toml'

    with open(toml_path,"rb") as file:
        metadata = tomli.load(file)
        SETTINGS_FILE = metadata["tool"]["path"]["setting_path"]
        KEY_FILE = metadata["tool"]["path"]["key_path"]
        launch_start = metadata["tool"]["config_system"]["launch_start"]
        defaul_start = metadata["tool"]["config_system"]["defaul_start"]
        display_console = metadata["tool"]["config_system"]["display_console"]

    #*  INIT LOGGER AND REQUEST_MAKER
    settings = init_settings()
    logger = Logger()
    request_maker = MakeRequests()

    #* CONST
    BANNER_MESSAGE = ['W','We','Wel','Welc','Welco','Welcom','Welcome','Welcome ',
                      'Welcome t','Welcome to','Welcome to ','Welcome to V',
                      'Welcome to Vi','Welcome to Vir','Welcome to Virg',
                      'Welcome to Virgi','Welcome to Virgil']
    SYSTEM = platform.system()
    ALERT = Style.BRIGHT + Fore.YELLOW
    OK = Style.BRIGHT + Fore.CYAN
    WARNIGN = Style.BRIGHT + Fore.RED

    main()
