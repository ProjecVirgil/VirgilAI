from pyttsx3 import *
import sys
import json
import openai

from prefix.creation import Log
from Moduls.timeNow import Time
from Moduls.ChanceValue import Value
from Moduls.TheWeather import WhatsIs
from Moduls.timeConv import TimeConversion
from Moduls.CalendarRec import Recoverycalendar,DayOfWeek
from Moduls.TheNews import news
from Moduls.TheLight import TurnTheLight

#init e setup the tts
engine = init("sapi5")
engine.setProperty("rate",180)
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)

#function for manage the command
#Preset command

#Start contest for GPT-3 API
messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata Dante e parli solo italiano."}
    ]

#Open file whith key api openai
with open("F:\ProjectDante\secret.json") as f:
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
    print("\nDante: Spegnimento in corso...")
    try:
        engine.say("Spegnimento in corso...")
        engine.runAndWait()
        sys.exit()
    except RuntimeError :
        print(Log(" Spegnimento con eccezione NO WARNING"))
        sys.exit()
    
def command(command:str):
    if(("spegniti" in command) or ("spegnimento" in command)):
        print(Log(" pre shut function"))
        off()
        
    elif((("ore" in command) or ("ora" in command)) and (("sono" in command) or ("è" in command))):
        print(Log(" pre time function"))
        res = Time.now()
        return res

        
    elif("volume" in command and (("imposta") in command or ("metti" in command) or ("inserisci")) ):
        print(Log(" pre volume function"))
        res = Value.change(command)
        if(res == 104):
            print("\nDante: Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10 ")
            engine.say("Non puoi dare un valore inferiore a 10, puoi dare solo valori da 100 a 10")
            engine.runAndWait()
            return None
        else:
            return res

        
    elif(("tempo fa" in command) or ("tempo fa a" in command) or ("che tempo fa" in command) or ("che tempo c'è" in command)):
        print(Log(" pre wheather function"))
        res = WhatsIs.TheWeather(command)
        return res

    elif((("gradi" in command ) or ("temperatura" in command)) and (("quanti" in command) or ("quanta" in command)) ):
        print(Log(" pre temperature function"))
        res = WhatsIs.Temp()
        return res


    elif("timer" in command and (("imposta" in command) or ("metti" in command) or ("crea" in command) )):
        print(Log(" pre timer function"))
        try:
            command = str(command).split(" di ")[1].strip()
            my_time = TimeConversion.conversion(command)
            return my_time
        except IndexError:
            print("Riprova a chiedere il comando perfavore")
            engine.say("Riprova a chiedere il comando perfavore")
            engine.runAndWait()
            return None
        
        #timer(command)
    elif("che giorno è" in command):
        print(Log(" pre recovery function"))
        lista=Recoverycalendar.recovery(command)
        if(len(lista) != 3):
            for x in range(3-len(lista)):
                lista.append(None)
        print(Log("Risultato: {lista}"))  
        giorno=lista[0]
        mese=lista[1]
        anno=lista[2]
        print(Log(" pre DayOfWeek function"))
        if( (mese != None ) and (anno != None) ):
            res = DayOfWeek.day(giorno,mese,anno)
        elif(mese == None and anno != None):
            res = DayOfWeek.day(giorno,anno=anno)
        elif(anno == None and mese != None):
            res = DayOfWeek.day(giorno,mese=mese)
        else:
            res = DayOfWeek.day(giorno)
        return res
    
    elif(( ("news" in command) or ("novità" in command) or ("notizie" in command) ) and (("parlami" in command) or ("dimmi" in command) or ("dammi" in command))):
        print(Log(" pre news function"))
        res = news.createNews(command)
        return res
    elif("luce" in command and (("accendi" in command) or ("spegni" in command) )):
        print(Log(" pre light function"))
        TurnTheLight.turn(command)
    #Question at GPT-3   
    else:
        print(Log(" GPT function"))
        messages.append({"role": "user", "content": command})
        new_message = get_response(messages=messages)
        print(Log(" risposta creata"))
        print(f"\nDante: {new_message['content']}")
        print(Log(" sto appendendo il comando..."))
        messages.append(new_message)
        print(Log(" comando appesso"))
        return new_message['content']

        

        

       