import datetime
import calendar
import calendar
import datetime

#from lib.prefix import Log 
#from lib.numberConvertToText import numberToWord

def numberToWord(number: str):
    # Definizione delle parole per i numeri da 0 a 19
    wordsUpToVents = [
        "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
        "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove", "venti"
    ]

    # Definizione delle parole per le decine
    wordDozens = [
        "", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"
    ]

    # Definizione delle parole per le centinaia
    wordHundreds = [
        "", "cento", "duecento", "trecento", "quattrocento", "cinquecento", "seicento", "settecento", "ottocento", "novecento"
    ]

    def convert_under_1000(number):
        if 0 <= number <= 999:
            if number < 21:
                return wordsUpToVents[number]
            elif number < 100:
                dozen = number // 10
                unit = number % 10
                # Regola di grammatica: se l'unità è 1 o 8, la decina perde l'ultima lettera
                if unit == 1 or unit == 8:
                    wordDozen = wordDozens[dozen][:-1]
                else:
                    wordDozen = wordDozens[dozen]
                if dozen == 1 and unit == 0:
                    return "dieci"
                elif dozen == 8 and unit == 0:
                    return "ottanta"
                else:
                    return wordDozen + wordsUpToVents[unit]
            else:
                hundred = number // 100
                remainder = number % 100
                if remainder == 0:
                    return wordHundreds[hundred]
                else:
                    return wordHundreds[hundred] + convert_under_1000(remainder)

    number = int(number)

    if 0 <= number <= 9999:
        if number < 1000:
            return convert_under_1000(number)
        else:
            thousands = number // 1000
            remainder = number % 1000
            result = ""
            if thousands == 1:
                result += "mille"
            else:
                result += wordsUpToVents[thousands] + "mila"
            if remainder > 0:
                if remainder < 100:
                    result += "e"
                result += convert_under_1000(remainder)
            return result

    return "Unmanaged number"


from colorama import Fore,Back
import inspect
import time


def Log(string: str, filepath: str = None):
    callstack = inspect.stack()[1]
    caller = str(inspect.getmodule(callstack[0])).split("\\")[-1]
    prfx=(Fore.GREEN + f"(in module {caller[:-2]}) " + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE)
    prfx = (prfx + " | ")
    log = prfx + string
    if filepath is not None:
        try:
            with open(filepath, "w") as f:
                f.write(log)
            return ''
        except IOError:
            return log
    return log



#ULTIMA DA LANCIARE
def recoverDayOfWeek(day:str,month:int = None, year:int = None):
    print(Log(" DayOfWeek function"))
    dayOfWeek= 0
    dateCurrente = datetime.datetime.now()
    if(month == None):
        month = dateCurrente.month
    if(year == None):
        year = dateCurrente.year
    for week in calendar.monthcalendar(year,month):
        for x in week:
            if( x == day):
                dayOfWeek=week.index(x)
    week = ["Lunedi","Martedi","Mercoledi","Giovedi","Venerdi","Sabato","Domenica"]
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    print(f"Il {day} di {month} del {year} è {week[dayOfWeek]}")
    if(day != 1):
        return f"Il {numberToWord(str(day))} di {months[month-1]} del {numberToWord(str(year))} è {str(week[dayOfWeek])}"
    else:
        return f"L'{numberToWord(str(day))} di {months[month-1]} del {numberToWord(str(year))} è {str(week[dayOfWeek])}"



def recoveryDateNumber(command:str):
    if(command == "che giorno e" or command == "che giorno e'"):
        day = str(datetime.datetime.now().date()).split('-')[2]
        listOfTime = [int(day),None,None]
        return listOfTime
    if(" il " in command):   
        query=command.split("il")[1].strip()
    elif(" e " in command):
        query=command.split(" e")[1].strip()
    elif(" era " in command):
        query=command.split(" era")[1].strip()
    else:
        query=command.split(" e'")[1].strip()
                
    divisionQuery = query.split(" ")
    listOfTime = []
    
    if(divisionQuery[0].isnumeric()):
        day=divisionQuery[0]
        listOfTime.append(int(day))
    else:
        if(divisionQuery[0] == "domani"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1) 
            day = tomorrow.day  
            listOfTime.append(day)
        elif(divisionQuery[0] == "ieri"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=-1) 
            day = tomorrow.day  
            listOfTime.append(day)
        elif(divisionQuery[0] == "oggi"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=0) 
            day = tomorrow.day  
            listOfTime.append(day)
        elif((divisionQuery[0] == "dopo") and (divisionQuery[1] == "domani") ):
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(days=2) 
                day = tomorrow.day 
                listOfTime.append(day)
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    thereAreMonth=True
    recoverMonth = ''
    for x in months:
        if(x in command):
            if("dopo domani" not in command):
                for month in months:
                    if(month in divisionQuery[1]):
                        recoverMonth = months.index(month) + 1
                listOfTime.append(recoverMonth)
                break
        '''else:
                for month in months:
                        if(month == divisionQuery[2] ):
                            recoverMonth = months.index(month) + 1
                listOfTime.append(recoverMonth)
                break'''
    else:
        thereAreMonth=False
    if(not thereAreMonth):
        return listOfTime
    try:
        if(divisionQuery[2].isnumeric):
            anno = divisionQuery[2]
            listOfTime.append(int(anno))
    except IndexError:
        listOfTime.append(None)
    return listOfTime
    
   
        
def splitTheDate(listOfDate:list):
    if(len(listOfDate) != 3):
        for _ in range(3-len(listOfDate)):
                listOfDate.append(None)
        print(Log(f" result: {listOfDate}"))  
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        return recoverDayOfWeek(day,month,year)
    else:
        print(Log(f" result: {listOfDate}")) 
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        print(day,month,year)
        print(Log(" pre dayOfWeek function"))
        if(month != None  and year != None ):
            return recoverDayOfWeek(day,month,year)
        elif(year == None and month != None):
            return  recoverDayOfWeek(day,month=month)
        else:
            return recoverDayOfWeek(day)
        

        
def getDate(command:str):
    dateNumber = recoveryDateNumber(command)
    print(dateNumber)
    result= splitTheDate(dateNumber)
    print(result)
    return result            

    
        
        
        
