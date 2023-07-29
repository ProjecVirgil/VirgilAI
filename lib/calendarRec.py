import datetime
import calendar
import calendar

from lib.prefix import Log 
from lib.numberConvertToText import numberToWord


# ---- File for get the week of the day ----


#ULTIMA DA LANCIARE
def recoverDayOfWeek(day:str,month:str,year:str):
    print(Log(" DayOfWeek function"))
    dayOfWeek= 0
    for week in calendar.monthcalendar(year,month):
        for x in week:
            if( x == day):
                dayOfWeek=week.index(x)
    week = ["Lunedi","Martedi","Mercoledi","Giovedi","Venerdi","Sabato","Domenica"]
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    print(f"Il {day} di {months[month-1]} del {year} è {week[dayOfWeek]}")
    if(day != 1):
        return f"Il {numberToWord(str(day))} di {months[month-1]} del {numberToWord(str(year))} è {str(week[dayOfWeek])}"
    else:
        return f"L'{numberToWord(str(day))} di {months[month-1]} del {numberToWord(str(year))} è {str(week[dayOfWeek])}"


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
    if(" il " in command or "il " in command):         
        query=command.split("il")[1].strip()
    elif(" e " in command):
        query=command.split(" e")[1].strip()
    elif(" era " in command):
        query=command.split(" era")[1].strip()
    elif(" al " in command):
        query=command.split(" al")[1].strip()
    elif(" all " in command):
        query=command.split(" al")[1].strip()
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
        print(Log(f" result: {listOfDate}"))  
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        return fillDate(day,month,year)
    else:
        print(Log(f" result: {listOfDate}")) 
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        print(Log(" pre dayOfWeek function"))
        if(month != None  and year != None ):
            return fillDate(day,month,year) #forse da fixare
        elif(year == None and month != None):
            return  fillDate(day,month=month) #forse da fixare
        else:
            return fillDate(day) #forse da fixare
        

        
def getDate(command:str):
    dateNumber = recoveryDateNumber(command)
    print(dateNumber)
    correctDay,correctMonth,correctYear = splitTheDate(dateNumber)
    result = recoverDayOfWeek(correctDay,correctMonth,correctYear)
    return result            

    
def getDiff(command:str):
    print(Log(" calculating the days..."),flush=True)
    dateNumber = recoveryDateNumber(command)
    correctDay,correctMonth,correctYear = splitTheDate(dateNumber)
    correct_date = datetime.datetime(correctYear, correctMonth, correctDay)
    diff_days = (datetime.datetime.now() - correct_date).days
    print(f" Al {correctDay} {correctMonth} {correctYear} mancano {diff_days * -1}")
    
    if(diff_days * -1 == 1):
        return f" Al {numberToWord(correctDay)} {numberToWord(correctMonth)} {numberToWord(correctYear)} manca un giorno"
    else:
        return f" Al {numberToWord(correctDay)}, {numberToWord(correctMonth)}, {numberToWord(correctYear)} mancano {numberToWord(diff_days * -1)} giorni"

    
    
        
        
