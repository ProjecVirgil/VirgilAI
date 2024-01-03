"""summary: The start file."""
import getpass
import sys
import time
import subprocess
import random
import os
import platform
import json

import pyfiglet
from colorama import Fore, Style
from plyer import notification
from winotify import Notification, audio

from lib.packages_utility.manager import ThreadManager
from lib.packages_utility.logger import logging
from lib.packages_utility.utils import init_settings
from lib.packages_utility.request import MakeRequests
from lib.packages_utility.db_manager import DBManagerSettings


# ---- This file launch all the file for making Virgilio work  ----


def check_system_clear():
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
        elif counter == 12:  # noqa: PLR2004
            delay = 0.25
        elif counter == 13:  # noqa: PLR2004
            delay = 0.3
        elif counter == 14:  # noqa: PLR2004
            delay = 0.35
        elif counter == 15:  # noqa: PLR2004
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
    request_maker.create_user_event(GLOBAL_KEY)
    logging.warning(f"KEEP YOUR KEY {GLOBAL_KEY} DON'T GIVE IT TO ANYONE")
    _ = input(logging.warning(
        'Now download the Virgil app on your Android device, go to the configuration page and enter this code in the appropriate field, once done you will be able to change all Virgil settings remotely, once done press any button: '))
    logging.info("Synchronizing your account settings")
    settings_json = request_maker.get_user_settings(GLOBAL_KEY)
    # INIT SETTING
    settings = init_settings(settings_json,GLOBAL_KEY)

    if settings == 'User not found':
        logging.error("User not found")
        logging.error(
            "There is a problem with your key try deleting it and restarting the launcher if the problem persists contact support")
        sys.exit(1)
    db_manager.create_update_user(GLOBAL_KEY, settings)
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
    settings = init_settings(settings_json,key)
    db_manager.create_update_user(key, settings)
    return settings

def show_notify():
    """Show all notifications from user mailbox."""
    if SYSTEM == 'Windows':
        toast = Notification(app_id="VirgilAI", title="Virgil AI NOTIFY",
                             msg="Virgil started correctly without errors", duration='long',
                             icon=os.path.join(os.getcwd(), 'assets', 'img', 'icon.ico'))
        toast.set_audio(audio.Mail, loop=False)
        toast.show()
    else:
        notification.notify(
            title='Virgil AI NOTIFY',
            message='Virgil AI started correctly without errors',
            timeout=10
        )
def main():  # noqa: PLR0915
    """Main function that will be called when running this script from command line."""
    command_cleaner = check_system_clear()
    print_banner(command_cleaner)
    rainbow(command_cleaner)
    install_libraries()
    logging.info(os.path.join(os.getcwd(), 'assets', 'img', 'icon.ico'))
    logging.info(f"PID PROCESS: {os.getpid()}")
    settings = create_account() if not db_manager.get_key() else log_in()
    logging.info("Threads initialization")
    manager = ThreadManager(settings, default_start)
    manager.init()
    logging.info("Threads start")
    manager.start()


# TODO ADD THE A FUNCTION TO INTERACT WITH GITHUB AND CHECK IF THE UPDATE  # noqa: TD002, FIX002, TD003, TD004
if __name__ == '__main__':
    subprocess.run("poetry install", shell=True, check=True)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    config_path = os.path.abspath(os.path.join('Users', getpass.getuser(), 'AppData', 'Local', 'Programs', 'Virgil-Installer',
                               'config.json'))
    with open(config_path) as file:
        config = json.load(file)

    default_start = config["type_interface"]
    display_console = config["display_console"]
    GLOBAL_KEY = config["key"]

    # *  INIT LOGGER AND REQUEST_MAKER
    request_maker = MakeRequests()
    db_manager = DBManagerSettings()
    db_manager.init()
    # * CONST
    BANNER_MESSAGE = ['W', 'We', 'Wel', 'Welc', 'Welco', 'Welcom', 'Welcome', 'Welcome ',
                      'Welcome t', 'Welcome to', 'Welcome to ', 'Welcome to V',
                      'Welcome to Vi', 'Welcome to Vir', 'Welcome to Virg',
                      'Welcome to Virgi', 'Welcome to Virgil']
    SYSTEM = platform.system()
    show_notify()
    main()
