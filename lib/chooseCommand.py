import sys
import json
import time
import psutil
import os 

import openai
import pygame


from lib.prefix import Log
from lib.sound import create
from lib.timeNow import now
from lib.changeValue import change
from lib.theWeather import TheWeather,Temp
from lib.timeConv import conversion
from lib.calendarRec import recovery,day
from lib.theNews import createNews
from lib.theLight import turn

#function for manage the command
#Preset command

#Start contest for GPT-3 API
messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata Virgilio e parli solo italiano."}
    ]
import os 
current_path = os.getcwd()
file_path = os.path.join(current_path,'secret.json')

#Open file whith key api openai
with open(file_path) as f:
    secrets = json.load(f)
    api_key = secrets["api"]
openai.api_key = api_key

#function for communicate whith api GPT-3
def get_response(messages:list):
    print(Log(" Sto creando la risposta..."))
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = 1.0 # 0.0 - 2.0
    )
    return response.choices[0].message

#shutdown function
def off():
    print(Log(" shut function"))
    print("\nVirgilio: Spegnimento in corso...")
    with open("connect/res.json", 'w') as file:
            data = {
                "0":["spento","spento",False]
            }
            json.dump(data,file,indent=4)
    time.sleep(2)
    sys.exit(0)
    
def Sendcommand(command:str):
    pygame.init()
    if(("spegniti" in command) or ("spegnimento" in command)):
        print(Log(" pre shut function"))
        off()
        
    elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("è" in command))):
        print(Log(" pre time function"))
        res = now()
        return res

    elif("stop" in command or "fermati" in command or "basta" in command):
        create("va bene mi fermo")
        
    elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
        print(Log(" pre volume function"))
        res = change(command)
        if(res == 104):
            print("\nVirgilio: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ")
            create("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
            return None
        else:
            return res

        
    elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command)):
        print(Log(" pre wheather function"))
        res = TheWeather(command)
        return res

    elif((("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command)) ):
        print(Log(" pre temperature function"))
        res = Temp(command)
        return res


    elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Log(" pre timer function"))
        try:
            command = str(command).split(" di ")[1].strip()
            my_time = conversion(command)
            return my_time
        except IndexError:
            print("Please try the command again")
            create("Please try the command again")
            return None
        
        #timer(command)
    elif("che giorno è" in command):
        print(Log(" pre recovery function"))
        lista=recovery(command)
        if(len(lista) != 3):
            for x in range(3-len(lista)):
                lista.append(None)
        print(Log("Risultato: {lista}"))  
        giorno=lista[0]
        mese=lista[1]
        anno=lista[2]
        print(Log(" pre DayOfWeek function"))
        if( (mese != None ) and (anno != None) ):
            res = day(giorno,mese,anno)
        elif(mese == None and anno != None):
            res = day(giorno,anno=anno)
        elif(anno == None and mese != None):
            res = day(giorno,mese=mese)
        else:
            res = day(giorno)
        return res
    
    elif(( ("news" in command) or ("novità" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
        print(Log(" pre news function"))
        res = createNews(command)
        return res
    elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
        print(Log(" pre light function"))
        turn(command)
    #Question at GPT-3   
    else:
        print(Log(" GPT function"))
        messages.append({"role": "user", "content": command})
        new_message = get_response(messages=messages)
        print(Log(" response created"))
        print(f"\nVirgilio: {new_message['content']}")
        print(Log(" I am hanging the command..."))
        messages.append(new_message)
        print(Log(" command append"))
        return new_message['content']
