import requests
from colorama import Style,Fore

from lib.logger import Logger  

ALERT = Style.BRIGHT + Fore.YELLOW
OK = Style.BRIGHT + Fore.CYAN
WARNIGN = Style.BRIGHT + Fore.RED
    


# ---- File for make the request at the VirgilAPI ----

class MakeRequests:
    
    def __init__(self) -> None:
        self.logger = Logger()
        self.URL_BASE = "https://fastapi-production-cd01.up.railway.app" + "/api"
        fileKey = open("setup/key.txt","r")
        self.ID = fileKey.read()    

    
    
    def createUser(self):
        #CREAZIONE USER
        url = f'{self.URL_BASE}/createUser'
        try:
            r = requests.put(url)
            UserCreated = r.json()
            print(self.logger.Log("User created Correctly"),flush=True)
            return UserCreated["userId"]
        except:
            print(self.logger.Log(WARNIGN + "I can't stable connection check the network"),flush=True)
        
        
    def getUser(self,id):
        url = f'{self.URL_BASE}/setting/{id}/'
        try:
            r = requests.get(url)
            user = r.json()
            if(user == {"Error": "User not found"}):
                return 'User not found'
            else:    
                return user['setting']
        except:
            print(self.logger.Log(WARNIGN + "I can't stable connection check the network"),flush=True)
        
        
    #CALENDAR

    ## Create user
    def createUserEvent(self,id):
        url = f'{self.URL_BASE}/calendar/createUser/{id}/'
        r = requests.put(url)
        if(r.status_code == 201):
            print(self.logger.Log("User calendar created correcly"),flush=True)
        else:
            print(self.logger.Log("User calendar offline"),flush=True)

    ## Create Event
    def createEvents(self,event:str,date:str):
        if("None" in date):
            print(self.logger.Log( "Sorry, but there was an error, the request will not be sent"),flush=True) 
        else:
            url = f'{self.URL_BASE}/calendar/createEvent/{self.ID}/{date}/'
            events = [event]
            print(events)
            headers = {'Content-Type': 'application/json'}
            r = requests.put(url, json=events,headers=headers)
            print(self.logger.Log(f" response: {r.status_code}"),flush=True)

    ## Get events
    def getEvents(self):
        url = f'{self.URL_BASE}/calendar/{self.ID}/'
        r = requests.get(url)
        print(self.logger.Log(f" reponse: {r.status_code}"),flush=True)
        events = r.json()
        return events

    def deleteEvents(self):
        url = f'{self.URL_BASE}/calendar/deleteEvent/{self.ID}/'
        r = requests.put(url)
        print(self.logger.Log(f" reponse: {r.status_code}"),flush=True)
        


