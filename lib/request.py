import datetime
import requests
from colorama import Style,Fore

from lib.prefix import Log  

ALERT = Style.BRIGHT + Fore.YELLOW
OK = Style.BRIGHT + Fore.CYAN
WARNIGN = Style.BRIGHT + Fore.RED
    
#TAKE KEY
fileKey = open("setup/key.txt","r")
id = fileKey.read()    
 
#USER
def createUser():
    #CREAZIONE USER
    url = 'https://flask-production-bb00.up.railway.app/api/createUser'
    try:
        r = requests.put(url)
        UserCreated = r.json()
        print(Log( "User created Correctly"))
        return UserCreated["userId"]
    except:
        print(Log(WARNIGN + "I can't stable connection check the network"))
    
    
def getUser(id):
    url = f'https://flask-production-bb00.up.railway.app/api/setting/{id}/'
    try:
        r = requests.get(url)
        user = r.json()
        if(user == {"Error": "User not found"}):
            return 'User not found'
        else:    
            return user['setting']
    except:
        print(Log(WARNIGN + "I can't stable connection check the network"))
    
    
#CALENDAR

## Create user
def createUserEvent(key):
    url = f'https://flask-production-bb00.up.railway.app/api/calendar/createUser/{key}/'
    r = requests.put(url)
    if(r.status_code == 201):
        print(Log(" User calendar created correcly"))
    else:
        print(Log(" User calendar offline"))

## Create Event
def createEvents(events:str,date:str):
    url = f'https://flask-production-bb00.up.railway.app/api/calendar/createEvent/{id}/{date}/'
    events = {
        date : [events]
    }
    headers = {'Content-Type': 'application/json'}
    r = requests.put(url,json=events,headers=headers)
    print(Log(f" response: {r.status_code}"))

## Get events
def getEvents():
    url = f'https://flask-production-bb00.up.railway.app/api/calendar/{id}/'
    r = requests.get(url)
    print(Log(f" reponse: {r.status_code}"))
    events = r.json()
    print(events)
    return events

def deleteEvents():
    url = f'https://flask-production-bb00.up.railway.app/api/calendar/deleteEvent/{id}/'
    r = requests.put(url)
    print(Log(f" reponse: {r.status_code}"))
    


