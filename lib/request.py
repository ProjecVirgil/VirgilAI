import requests
from colorama import Style,Fore
from lib.prefix import Log  

ALERT = Style.BRIGHT + Fore.YELLOW
OK = Style.BRIGHT + Fore.CYAN
WARNIGN = Style.BRIGHT + Fore.RED
    
def createUser():
    #CREAZIONE USER
    url = 'https://flask-production-bb00.up.railway.app/api/createUser'
    try:
        r = requests.put(url)
        UserCreated = r.json()
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
    





