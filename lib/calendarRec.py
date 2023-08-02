import datetime
import calendar


from lib.sound import Audio
from lib.logger import Logger
from lib.utils import Utils


# ---- File for get the week of the day ----


#ULTIMA DA LANCIARE

logger = Logger()
utils = Utils()
audio = Audio()

def recoverDayOfWeek(day:str,month:str,year:str):
    print(logger.Log(" DayOfWeek function"), flush=True)
    dayOfWeek= 0
    for week in calendar.monthcalendar(year,month):
        for x in week:
            if( x == day):
                dayOfWeek=week.index(x)
    week = ["Lunedi","Martedi","Mercoledi","Giovedi","Venerdi","Sabato","Domenica"]
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    print(f"Il {day} di {months[month-1]} del {year} è {week[dayOfWeek]}", flush=True)
    
    if((day == None or day == '' ) or month == None or year ==  None ):
        print("Mi dispiace ma non sono riuscito a capire bene la data puoi rifare la domanda",flush=True)
        audio.create(file=True,namefile="ErrorDate")
    else:
        if(day != 1):
            return f"Il {utils.numberToWord(str(day))} di {months[month-1]} del {utils.numberToWord(str(year))} è {str(week[dayOfWeek])}"
        else:
            return f"L'{utils.numberToWord(str(day))} di {months[month-1]} del {utils.numberToWord(str(year))} è {str(week[dayOfWeek])}"


def fillDate(day:str,month:int = None, year:int = None):
    dateCurrente = datetime.datetime.now()
    if(month == None):
        month = dateCurrente.month
    if(year == None):
        year = dateCurrente.year
        
    return day,month,year


def recoveryDateNumber(command:str):
    if(command == "che giorno e" or command == "che giorno e'"):
        day = str(datetime.datetime.now().date()).split('-')[2]
        listOfTime = [int(day),None,None]
        return listOfTime
    try:
        if(" il " in command or "il " in command):         
            query=command.split("il")[1].strip()
        elif(" e " in command):
            query=command.split(" e")[1].strip()
        elif(" sara' " in command):
            query=command.split(" sara'")[1].strip()
        elif(" sara " in command):
            query=command.split(" sara")[1].strip()
        elif(" era " in command):
            query=command.split(" era")[1].strip()
        elif(" al " in command):
            query=command.split(" al")[1].strip()
        elif(" all " in command):
            query=command.split(" al")[1].strip()
        else:
            query=command.split(" e'")[1].strip()
    except IndexError:
        return "ERROR"
                
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
    else:
        thereAreMonth=False
    if(not thereAreMonth):
        return listOfTime
    try:
        if(divisionQuery[2].isnumeric()):
            anno = divisionQuery[2]
            listOfTime.append(int(anno))
        else:
            listOfTime.append(None)
    except IndexError:
        listOfTime.append(None)
    return listOfTime
    
   
        
def splitTheDate(listOfDate:list):
    if(len(listOfDate) != 3):
        for _ in range(3-len(listOfDate)):
                listOfDate.append(None)
        print(logger.Log(f" result: {listOfDate}"), flush=True)  
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        return fillDate(day,month,year)
    else:
        print(logger.Log(f" result: {listOfDate}"), flush=True)
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        print(logger.Log(" pre dayOfWeek function"), flush=True)
        if(month != None  and year != None ):
            return fillDate(day,month,year) #forse da fixare
        elif(year == None and month != None):
            return  fillDate(day,month=month) #forse da fixare
        else:
            return fillDate(day) #forse da fixare
        

        
def getDate(command:str):
    dateNumber = recoveryDateNumber(command)
    if(dateNumber == "ERROR"):
        print("Mi dispiace, c'è stato un errore prova a rifarmi la domanda in maniera piu precisa, specifica il giorno",flush=True)
        audio.create(file=True,namefile="ErrorRecoveryDay")
        return None

    correctDay,correctMonth,correctYear = splitTheDate(dateNumber)
    result = recoverDayOfWeek(correctDay,correctMonth,correctYear)
    return result            

    
def getDiff(command:str):
    print(logger.Log(" calculating the days..."),flush=True)
    dateNumber = recoveryDateNumber(command)
    if(dateNumber == "ERROR"):
        print("Mi dispiace, c'è stato un errore prova a rifarmi la domanda in maniera piu precisa, specifica il giorno",flush=True)
        audio.create(file=True,namefile="ErrorRecoveryDay")
        return None
    correctDay,correctMonth,correctYear = splitTheDate(dateNumber)
    correct_date = datetime.datetime(correctYear, correctMonth, correctDay)
    diff_days = (datetime.datetime.now() - correct_date).days
    print(f" Al {correctDay} {correctMonth} {correctYear} mancano {diff_days * -1}", flush=True)
    
    if(diff_days * -1 == 1):
        return f" Al {utils.numberToWord(correctDay)} {utils.numberToWord(correctMonth)} {utils.numberToWord(correctYear)} manca un giorno"
    else:
        return f" Al {utils.numberToWord(correctDay)}, {utils.numberToWord(correctMonth)}, {utils.numberToWord(correctYear)} mancano {utils.numberToWord(diff_days * -1)} giorni"

    
    
        
        
