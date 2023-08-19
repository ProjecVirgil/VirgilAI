"""_summary_

    Returns:
        _type_: _description_
"""
import requests
from colorama import Style,Fore

from lib.logger import Logger

ALERT = Style.BRIGHT + Fore.YELLOW
OK = Style.BRIGHT + Fore.CYAN
WARNIGN = Style.BRIGHT + Fore.RED

# ---- File for make the request at the VirgilAPI ----

class MakeRequests:
    """_summary_
    """
    def __init__(self) -> None:
        self.logger = Logger()
        self.url_base = "https://fastapi-production-cd01.up.railway.app" + "/api"
        with open("setup/key.txt","r",encoding="utf8") as file_key:
            self.key_user = file_key.read()

    def create_user(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        #CREAZIONE USER
        url = f'{self.url_base}/createUser'
        try:
            request = requests.put(url,timeout=5)
            user_created = request.json()
            print(self.logger.log("User created Correctly"),flush=True)
            return user_created["userId"]
        except requests.RequestException:
            print(self.logger.log(WARNIGN + "I can't stable connection check the network"),
                  flush=True)
            return "User not created"

    def get_user(self,key_user):
        """_summary_

        Args:
            id (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = f'{self.url_base}/setting/{key_user}/'
        try:
            request = requests.get(url,timeout=5)
            user = request.json()
            if user == {"Error": "User not found"}:
                return 'User not found'
            return user['setting']
        except requests.RequestException:
            print(self.logger.log(WARNIGN + "I can't stable connection check the network")
                  ,flush=True)
            return "Error in the request sorry"


    #CALENDAR

    ## Create user
    def create_user_event(self,key_user):
        """_summary_

        Args:
            id (_type_): _description_
        """
        url = f'{self.url_base}/calendar/createUser/{key_user}/'
        request = requests.put(url,timeout=5)
        if request.status_code == 201:
            print(self.logger.log("User calendar created correcly"),flush=True)
        else:
            print(self.logger.log("User calendar offline"),flush=True)

    ## Create Event
    def create_events(self,event:str,date:str):
        """_summary_

        Args:
            event (str): _description_
            date (str): _description_
        """
        if "None" in date:
            print(self.logger.log( "Sorry, but there was an error, the request will not be sent"),
                  flush=True)
        else:
            url = f'{self.url_base}/calendar/createEvent/{self.key_user}/{date}/'
            events = [event]
            headers = {'Content-Type': 'application/json'}
            request = requests.put(url, json=events,headers=headers,timeout=5)
            print(self.logger.log(f" response: {request.status_code}"),flush=True)

    ## Get events
    def get_events(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        url = f'{self.url_base}/calendar/{self.key_user}/'
        request = requests.get(url,timeout=5)
        print(self.logger.log(f" reponse: {request.status_code}"),flush=True)
        events = request.json()
        return events

    def delete_events(self):
        """_summary_
        """
        url = f'{self.url_base}/calendar/deleteEvent/{self.key_user}/'
        request = requests.put(url,timeout=5)
        print(self.logger.log(f" reponse: {request.status_code}"),flush=True)
