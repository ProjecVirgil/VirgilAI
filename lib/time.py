import datetime
from lib.prefix import Log
from lib.numberConvertToText import numberToWord 
import time


# ---- This file get the current time and more ----


def now():
    print(Log(" Time function"),flush=True)
    timeTuple = time.localtime() # get struct_time
    hours = time.strftime('%H',timeTuple)
    minuts = time.strftime('%M',timeTuple)
    hoursToWords = numberToWord(hours)
    minutsToWords = numberToWord(minuts)
    timeString = (f"Sono le {str(hoursToWords)} e {str(minutsToWords)}  minuti")
    print(time.strftime("\nVirgilio: Sono le %H e %M minuti", timeTuple),flush=True)
    return timeString


def diffTime(command:str):
    currentTime = datetime.datetime.now().time()
    if(" al " in command):
        query=command.split(" al")[1].strip()
    elif(" alle " in command):
        query=command.split(" alle")[1].strip()
    elif(" per le " in command):
        query=command.split(" le")[1].strip()

        
    querySplitted = query.split(" e ")
    
    hours = querySplitted[0]
    minuts = querySplitted[1]
    timeString = f"{hours}:{minuts}"
    
    timeFormatted = datetime.datetime.strptime(timeString, "%H:%M").time()

    data_corrente = datetime.datetime.combine(datetime.date.today(), currentTime)
    data_specificata = datetime.datetime.combine(datetime.date.today(), timeFormatted)

    diff_time = data_specificata - data_corrente

    calculatedHours, rest = divmod(diff_time.seconds, 3600)
    calculatedMinuts, calculateSeconds = divmod(rest, 60)

    if("sveglia" in command):
        print(Log( f" tempo calcolato per la sveglia {calculatedHours},{calculatedMinuts},{calculateSeconds}"),flush=True)
        return f"{calculatedHours} ore {calculatedMinuts} minuti e {calculateSeconds} secondi"
    else:
        print(Log(f" alle {numberToWord(hours)} e {numberToWord(minuts)} mancano {numberToWord(calculatedHours)} {numberToWord(calculatedMinuts)} {numberToWord(calculateSeconds)}"),flush=True)
        return f" alle {numberToWord(hours)} e {numberToWord(minuts)} mancano {numberToWord(calculatedHours)} ore {numberToWord(calculatedMinuts)} minuti e {numberToWord(calculateSeconds)} secondi"
    # Stampa la differenza in un formato più comprensibile
    


    
    

