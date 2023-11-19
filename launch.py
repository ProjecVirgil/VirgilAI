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
from colorama import Fore, Style

import lib.packages_utility.logger
import logging
from lib.packages_utility.utils import init_settings
from lib.packages_utility.vectorize import GloVeVectorizer, sentence_to_vec  # noqa: F401
from lib.packages_utility.request import MakeRequests


# ---- This file launch all the file for making Virgilio work  ----


def check_system():
    """Check if system is windows or linux and return a string with it is name clear command.

    Returns:
        str or int: If the system is recognize return a correct command for the OS
    """
    if SYSTEM == 'Windows':
        return "cls"
    if SYSTEM in ('Darwin', 'Linux'):
        return "clear"
    logging.critical(" Unrecognized operating system.Unable to start the corresponding terminal"),
    sys.exit(1)
    return 404


def print_banner(command_cleaner: str):
    """Print the main banner of Virgil.

    Args: COMMAND_CLEANER (str): The command for clear the console
    """
    delay = 0.1
    counter = 0
    for i in BANNER_MESSAGE:
        subprocess.run(command_cleaner, shell=True, check=False)
        print(Style.BRIGHT + Fore.MAGENTA + pyfiglet.figlet_format(i), flush=True)
        if counter == 11:
            delay = 0.2
        elif counter == 12:
            delay = 0.25
        elif counter == 13:
            delay = 0.3
        elif counter == 14:
            delay = 0.35
        elif counter == 15:
            delay = 0.4
        time.sleep(delay)
        counter += 1


def rainbow(command_cleaner: str):
    """Animation rainbow on the first banner.

    Args: command cleaner (str): The command for clear the console
    """
    delay = 0.1
    color = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    for _ in range(16):
        subprocess.run(command_cleaner, shell=True, check=False)
        print(
            Style.BRIGHT +
            random.choice(color) +
            pyfiglet.figlet_format(BANNER_MESSAGE[-1]), flush=True
        )
        time.sleep(delay)
    subprocess.run(command_cleaner, shell=True, check=False)
    print(Style.BRIGHT + Fore.MAGENTA + pyfiglet.figlet_format(BANNER_MESSAGE[-1]),
          flush=True)


def install_libraries():
    """Install and check all libraries needed by virgil.

    #TODO to change on a check update function
    """
    logging.info("START CHECK THE LIBRARY")


def create_account() -> str:
    """Create a new account with Virgil API.

    Returns:
        str: return the key of account created

    """
    logging.info("I am creating your synchronization key")
    key = request_maker.create_user()
    request_maker.create_user_event(key)

    logging.warning(f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE")

    with open(KEY_FILE, 'w', encoding="utf8") as file_key:
        file_key.write(str(key))
    _ = input(logging.warning(
        'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '))
    logging.info("Synchronizing your account settings")
    user = request_maker.get_user_settings(key)

    with open(SETTINGS_FILE, 'w', encoding="utf8") as file_setting:
        json.dump(user, file_setting, indent=4)

    if user == 'User not found':
        logging.error("User not found")
        logging.error(
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support")
        sys.exit(1)
    return key


def log_in() -> str:
    """Log in to an existing account using its private key saved on disk (setup/key.txt).

    Returns:
        str: return the key of account created
    """
    with open(KEY_FILE, encoding="utf8") as file_key:
        logging.info("I pick up the key for synchronization")
        key = file_key.readline()
        logging.info("Synchronizing your account settings")
        user = request_maker.get_user_settings(key)
    with open(SETTINGS_FILE, 'w', encoding="utf8") as file_setting:
        json.dump(user, file_setting, indent=4)
    if user == 'User not found':
        logging.error("User not found")
        logging.error(
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),
        sys.exit(1)
    return key


def choise_input():
    """This function is used when you want to choose between the text input or Voice input.

    Returns:
        str: the type of input
    """
    while True:
        text_or_speech = str(input(
            Fore.GREEN + Style.BRIGHT + "You want a text interface (T) or recognise interface(R) T/R: " + Style.RESET_ALL)).upper()
        if text_or_speech == 'T':
            return 1
        elif text_or_speech == 'R':
            return 0
        else:
            logging.warning(" Select a valid choice please")


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

    logging.info(f"PID PROCESS: {os.getpid()}")

    key = create_account() if os.path.getsize(KEY_FILE) == 0 or not os.path.exists(KEY_FILE) else log_in()
    #INIT SETTING
    settings = init_settings()

    if not os.path.exists("model/model_en.pkl"):
        logging.info("Start the download of english model this operation will take some time, but will only be done "
                     "once ")
        request_maker.download_model_en()
        logging.info(" Download finish")

    # *INIT ALL PRINCIPLE CLASS

    output = Output(settings)
    process = Process(settings)
    text_input = TextInput(settings)
    vocal_input = VocalInput(settings)
    thread_1 = 0
    thread_2 = 0
    thread_3 = 0
    if default_start == 'N':
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
            logging.warning(" Select a valid choice please")
    elif default_start == 'T':
        thread_1 = threading.Thread(target=text_input.text)
        thread_2 = threading.Thread(target=process.main)
        thread_3 = threading.Thread(target=output.out)
    else:
        thread_1 = threading.Thread(target=vocal_input.listening)
        thread_2 = threading.Thread(target=process.main)
        thread_3 = threading.Thread(target=output.out)

    logging.info("PROGRAM IN EXECUTION")
    logging.info(" THE PROGRAMMES WILL START SOON")
    thread_1.start()
    logging.info(" INPUT THREAD START...")
    thread_2.start()
    logging.info(" PROCESS THREAD START...")
    thread_3.start()
    logging.info(" OUTPUT THREAD START...")

# TODO ADD THE A FUNCTION TO INTERACT WITH GITHUB AND CHECK IF THE UPDATE
# COPIA CONFRONTA FA PARTIRE UN BASH CHE COPIA O QUALCOSA DI SIMILE
if __name__ == '__main__':
    # Update dependes command
    subprocess.run("poetry update",shell=True,check=True)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    toml_path = 'pyproject.toml'
    with open(toml_path, "rb") as file:
        metadata = tomli.load(file)
        SETTINGS_FILE = metadata["tool"]["path"]["setting_path"]
        KEY_FILE = metadata["tool"]["path"]["key_path"]
        launch_start = metadata["tool"]["config_system"]["launch_start"]
        default_start = metadata["tool"]["config_system"]["defaul_start"]
        display_console = metadata["tool"]["config_system"]["display_console"]

    # *  INIT LOGGER AND REQUEST_MAKER
    request_maker = MakeRequests()
    # * CONST
    BANNER_MESSAGE = ['W', 'We', 'Wel', 'Welc', 'Welco', 'Welcom', 'Welcome', 'Welcome ',
                      'Welcome t', 'Welcome to', 'Welcome to ', 'Welcome to V',
                      'Welcome to Vi', 'Welcome to Vir', 'Welcome to Virg',
                      'Welcome to Virgi', 'Welcome to Virgil']
    SYSTEM = platform.system()
    main()
