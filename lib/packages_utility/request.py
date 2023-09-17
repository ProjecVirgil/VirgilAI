""""""
import requests
from colorama import Style,Fore

from lib.packages_utility.logger import Logger

ALERT = Style.BRIGHT + Fore.YELLOW
OK = Style.BRIGHT + Fore.CYAN
WARNIGN = Style.BRIGHT + Fore.RED

# ---- File for make the request at the VirgilAPI ----

class MakeRequests:
    """
    This class is responsible to make all requests of the application.
    """
    def __init__(self) -> None:
        self.logger = Logger()
        self.url_base = "https://fastapi-production-cd01.up.railway.app" + "/api"
        with open("setup/key.txt","r",encoding="utf8") as file_key:
            self.key_user = file_key.read()

    def create_user(self) -> str:
        """
        This function creates a user in the database and returns its id if it was created successfully or an error message otherwise

        Returns:
            str: Return the result of the request
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

    def get_user_settings(self,key_user) -> str:
        """
        This function makes a GET request to the API and returns the settings

        Args:
            id (_type_): the id of the user

        Returns:
            str: result of request or the user settings 
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
    def create_user_event(self,key_user)-> str:
        """
        This function creates an event for the user with the key passed as parameter

        Args:
            id (_type_): the id of user
        """
        url = f'{self.url_base}/calendar/createUser/{key_user}/'
        request = requests.put(url,timeout=5)
        if request.status_code == 201:
            print(self.logger.log("User calendar created correcly"),flush=True)
        else:
            print(self.logger.log("User calendar offline"),flush=True)

    def create_events(self,event:str,date:str)-> str:
        """
        This function creates events for the users that are registered on the system

        Args:
            event (str): the events to add
            date (str): the date of events to add
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

    def get_events(self)-> str:
        """
        Get the events of the day

        Returns:
            list: list of all events
        """
        url = f'{self.url_base}/calendar/{self.key_user}/'
        request = requests.get(url,timeout=5)
        print(self.logger.log(f" reponse: {request.status_code}"),flush=True)
        events = request.json()
        return events

    def delete_events(self)-> str:
        """
        Delete the old events
        """
        url = f'{self.url_base}/calendar/deleteEvent/{self.key_user}/'
        request = requests.put(url,timeout=5)
        print(self.logger.log(f" reponse: {request.status_code}"),flush=True)

    def download_model_en(self):
        """
        Download model english
        """
        url = "https://filemodelen.s3.eu-north-1.amazonaws.com/model_en.pkl"
        destination = 'model/model_en.pkl'
        response = requests.get(url,stream=True,timeout=None)
        with open(destination, 'wb') as file:
            file.write(response.content)
