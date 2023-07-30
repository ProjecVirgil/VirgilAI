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


URL_BASE = "http://fastapi-production-cd01.up.railway.app" + "/api"
# ---- File for make the request at the VirgilAPI ----


def createUser():
    #CREAZIONE USER
    url = f'{URL_BASE}/createUser'
    try:
        r = requests.put(url)
        UserCreated = r.json()
        print(Log( "User created Correctly"),flush=True)
        return UserCreated["userId"]
    except:
        print(Log(WARNIGN + "I can't stable connection check the network"),flush=True)
    
    
def getUser(id):
    url = f'{URL_BASE}/setting/{id}/'
    try:
        r = requests.get(url)
        user = r.json()
        if(user == {"Error": "User not found"}):
            return 'User not found'
        else:    
            return user['setting']
    except:
        print(Log(WARNIGN + "I can't stable connection check the network"),flush=True)
    
    
#CALENDAR

## Create user
def createUserEvent(key):
    url = f'{URL_BASE}/calendar/createUser/{key}/'
    r = requests.put(url)
    if(r.status_code == 201):
        print(Log(" User calendar created correcly"),flush=True)
    else:
        print(Log(" User calendar offline"),flush=True)

## Create Event
def createEvents(event:str,date:str):
    if("None" in date):
        print(Log( "Sorry, but there was an error, the request will not be sent"),flush=True) 
    else:
        url = f'{URL_BASE}/calendar/createEvent/{id}/{date}/'
        #events = [event]
        events = { #DA CANCELLARE APPENA RITORNA UP RAILWAY
            date:[event]
        }

        headers = {'Content-Type': 'application/json'}
        r = requests.put(url,json=events,headers=headers)
        print(Log(f" response: {r.status_code}"),flush=True)

## Get events
def getEvents():
    url = f'{URL_BASE}/calendar/{id}/'
    r = requests.get(url)
    print(Log(f" reponse: {r.status_code}"),flush=True)
    events = r.json()
    return events

def deleteEvents():
    url = f'{URL_BASE}/calendar/deleteEvent/{id}/'
    r = requests.put(url)
    print(Log(f" reponse: {r.status_code}"),flush=True)
    


