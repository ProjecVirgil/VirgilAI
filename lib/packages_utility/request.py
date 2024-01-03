"""File to manage all the request at the VirgilAPI."""
import requests
import re
from lib.packages_utility.logger import logging


# ---- File for make the request at the VirgilAPI ----

class MakeRequests:
    """This class is responsible to make all requests of the application."""

    def __init__(self,language:str="None") -> None:
        """Init file for sett the url and init the logger class."""
        self.url_base = "https://virgilapi-production.up.railway.app" + "/api"
        self.prompt = f"In the context of the following sentence, answer using only two letters from the options: OR for current time requests, VL for volume changes, MT for weather requests, TM for timer start requests, GDS for day of the week requests, MC for counting days to a specific day, NW for news or latest updates, MU for music start requests, EV for adding events to the calendar, and AL for all other requests. The language the input will be in is {'english' if language == 'en' else 'italian'}"
        self.headers_model = { #I KNOW THIS KEY IS EXPOSE BUT IS SIMPLE KEY TEST
                "Content-Type": "application/json",
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiI1MGNkMWM1MS0zNmEzLTQwYTItYWJlOS1jYzMzZmUyOGUwZGIiLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiJlZTUwM2I4OS0wYWFkLTRhNzgtYmJlZi0zZGE4OGQ3MWMwNWUiLCJ1c2VySWQiOiJiZjk3Y2M3My0wZTRmLTQ0NTgtOGY4Mi1mODk1YzZhM2JjYmYiLCJyb2xlcyI6WyJGRVRDSC1ST0xFUy1CWS1BUEkiXSwicGVybWlzc2lvbnMiOlsiRkVUQ0gtUEVSTUlTU0lPTlMtQlktQVBJIl0sImF1ZCI6IjNkMjMzOTQ5LWEyZmItNGFiMC1iN2VjLTQ2ZjYyNTVjNTEwZSIsImlzcyI6Imh0dHBzOi8vaWRlbnRpdHkub2N0b21sLmFpIiwiaWF0IjoxNzA0MTkyMjgxfQ.W6JoeyGV5WXjEEhOF7Kk7UHyYua6hr-NAVXahGmSdNRcws7OtKdYb-Aj3f-czNHcJmOGTSEymuHkdAkuMUuHztseInIRWThyZ6rqYawFTaltT_LjGK2wbH2IJb2BZuz3M-_KaogjPBz88-o4lI-grjv_6SYz0Qndy_2E0F9FgLxkh5abu9mAL1SNeg076pDGFy-xaag3tfUbL_XVmjsp-k806ucmTeZt0iCJ_LpYWPjBdn-JZs2QMyNPFUEhT_Sif5pcUYzWtIYD3oBIuhjKnwrDOsxQce0jAGjr9vSv-I1tDw667H2s50PnZGVZ9RDQYT4dQzzQTPVxjQOVvAiCFw"
            }
        self.url_model = "https://text.octoai.run/v1/chat/completions"


    def get_user_settings(self, key_user) -> str:
        """This function makes a GET request to the API and returns the settings.

        Args:
            key_user (str): the id of the user

        Returns:
            str: result of request or the user settings
        """
        url = f'{self.url_base}/setting/{key_user}/'
        try:
            request = requests.get(url, timeout=5)
            user = request.json()
            if user == {"Error": "User not found"}:
                return 'User not found'
            return user['setting']
        except requests.RequestException:
            logging.critical("I can't stable connection check the network")
            return "Error in the request sorry"

    # CALENDAR
    def create_user_event(self, key_user):
        """This function creates an event for the user with the key passed as parameter.

        Args:
            key_user (_type_): the id of user
        """
        url = f'{self.url_base}/calendar/createUser/{key_user}/'
        request = requests.put(url, timeout=5)
        value_success = 201

        if request.status_code == value_success:
            logging.info("User calendar created correctly")
        else:
            logging.warning("User calendar offline")

    def create_events(self, event: str, date: str,key_user):
        """This function creates events for the users that are registered on the system.

        Args:
            event (str): the events to add
            date (str): the date of events to add
            key_user (str): the id of the user
        """
        if "None" in date:
            logging.error("Sorry, but there was an error, the request will not be sent")
        else:
            url = f'{self.url_base}/calendar/createEvent/{key_user}/{date}/'
            events = [event]
            headers = {'Content-Type': 'application/json'}
            request = requests.put(url, json=events, headers=headers, timeout=5)
            logging.debug(f" response: {request.status_code}")

    def get_events(self,key_user) -> str:
        """Get the events of the day.

        Args:
            key_user (str): the id of the user

        Returns:
            list: list of all events
        """
        url = f'{self.url_base}/calendar/{key_user}/'
        request = requests.get(url, timeout=5)
        logging.debug(f" response: {request.status_code}")
        events = request.json()
        return events

    def delete_events(self,key_user):
        """Delete the old events."""
        url = f'{self.url_base}/calendar/deleteEvent/{key_user}/'
        request = requests.put(url, timeout=5)
        logging.debug(f" response: {request.status_code}")

    def clean_output_models(self,input:str) -> str:
        """This method cleans the output from models and returns a string without special characters or numbers.

        Args:
            input (str): The input

        Returns:
            str: The input cleaned
        """
        return re.sub('[^a-zA-Z]', '', input.upper().strip())

    def get_category(self,input:str) -> str:
        """This method is used to find out what category a word belongs to using the trained machine learning model.

        Args:
            input (str): _description_

        Returns:
            _type_: _description_
        """
        data = {
                "messages": [
                    {
                        "role": "system",
                        "content": self.prompt
                    },
                    {
                        "role": "user",
                        "content": input
                    }
                ],
                "model": "mixtral-8x7b-instruct-fp16",
                "max_tokens": 2,
                "presence_penalty": 0,
                "temperature": 0.1,
                "top_p": 0.9
            }

        response = requests.post(self.url_model, headers=self.headers_model, json=data).json()
        logging.debug(f"Response of model: {response}")
        return  self.clean_output_models(response['choices'][0]['message']['content'])
