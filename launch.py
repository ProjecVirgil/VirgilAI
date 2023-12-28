"""summary: The start file."""
import sys
import time
import subprocess
import random
import os
import platform

import tomli
import pyfiglet
from colorama import Fore, Style

from lib.packages_main.manager import ThreadManager
import lib.packages_utility.logger  # noqa: F401
import logging
from lib.packages_utility.utils import init_settings
from lib.packages_utility.vectorize import GloVeVectorizer, sentence_to_vec  # noqa: F401
from lib.packages_utility.request import MakeRequests
from lib.packages_utility.db_manager import DBManager


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
        if counter == 11:  # noqa: PLR2004
            delay = 0.2
        elif counter == 12: # noqa: PLR2004
            delay = 0.25
        elif counter == 13: # noqa: PLR2004
            delay = 0.3
        elif counter == 14: # noqa: PLR2004
            delay = 0.35
        elif counter == 15: # noqa: PLR2004
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


def create_account():
    """Create a new account with Virgil API.

    Returns:
        str: return the key of account created

    """
    logging.info("I am creating your synchronization key")
    key = request_maker.create_user()
    request_maker.create_user_event(key)
    logging.warning(f"KEEP YOUR KEY {key} DON'T GIVE IT TO ANYONE")
    _ = input(logging.warning(
        'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '))
    logging.info("Synchronizing your account settings")
    settings_json = request_maker.get_user_settings(key)
    #INIT SETTING
    settings = init_settings(settings_json)

    if settings == 'User not found':
        logging.error("User not found")
        logging.error(
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support")
        sys.exit(1)
    db_manager.create_update_user(key,settings)
    return settings


def log_in():
    """Log in to an existing account using its private key saved on disk (setup/key.txt).

    Returns:
        str: return the key of account created
    """
    logging.info("I pick up the key for synchronization")
    logging.info("Synchronizing your account settings")
    key = db_manager.get_key()
    settings_json = request_maker.get_user_settings(key)
    if settings_json == 'User not found':
        logging.error("User not found")
        logging.error(
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support"),
        sys.exit(1)
    settings = init_settings(settings_json)
    db_manager.create_update_user(key,settings)
    return settings



def main():  # noqa: PLR0915
    """Main function that will be called when running this script from command line."""
    command_cleaner = check_system()
    print_banner(command_cleaner)
    rainbow(command_cleaner)
    install_libraries()


    logging.info(f"PID PROCESS: {os.getpid()}")
    settings = create_account() if not db_manager.get_key() else log_in()

    if not os.path.exists("model/model_en.pkl"):
        logging.info("Start the download of english model this operation will take some time, but will only be done "
                     "once ")
        request_maker.download_model_en()
        logging.info(" Download finish")

    manager = ThreadManager(settings,default_start)
    manager.init()
    manager.start()

# TODO ADD THE A FUNCTION TO INTERACT WITH GITHUB AND CHECK IF THE UPDATE  # noqa: TD002, FIX002, TD003, TD004
if __name__ == '__main__':
    # Update depends command

    #ADD TRY
    subprocess.run("poetry install",shell=True,check=True)
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
    db_manager = DBManager()
    db_manager.init()
    # * CONST
    BANNER_MESSAGE = ['W', 'We', 'Wel', 'Welc', 'Welco', 'Welcom', 'Welcome', 'Welcome ',
                      'Welcome t', 'Welcome to', 'Welcome to ', 'Welcome to V',
                      'Welcome to Vi', 'Welcome to Vir', 'Welcome to Virg',
                      'Welcome to Virgi', 'Welcome to Virgil']
    SYSTEM = platform.system()
    main()
