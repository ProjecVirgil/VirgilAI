import requests

def createUser():
    #CREAZIONE USER
    url = 'https://flask-production-bb00.up.railway.app/api/createUser'
    r = requests.put(url)
    UserCreated = r.json()
    return UserCreated["userId"]
    
def getUser(id):
    url = f'https://flask-production-bb00.up.railway.app/api/setting/{id}/'
    r = requests.get(url)
    user = r.json()
    return user





