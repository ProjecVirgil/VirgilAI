import datetime
import calendar
import calendar
import datetime

from lib.prefix import Log 

def dayOfWeek(day:str,month:int = None, year:int = None):
    print(Log(" DayOfWeek function"))
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
    result = f"Il {day} di {month} del {year} è {week[dayOfWeek]}"
    print(f"Il {day} di {month} del {year} è {week[dayOfWeek]}")
    return result



def recoveryDate(command:str):
    
    if(command == "mi dici che giorno e"):
        day = datetime.datetime.today()
        listOfTime = [day,None,None]
        return listOfTime
    
    if(" il " in command):   
        query=command.split(" il ")[1].strip()
    else:
        query=command.split(" è ")[1].strip()
        
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
        elif((divisionQuery[0] == "dopo") and (divisionQuery[1] == 'domani') ):
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(days=2) 
                day = tomorrow.day 
                listOfTime.append(day)
    
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    bool=True
    
    for x in months:
        if(x in command):
            if("dopo domani" not in command):
                for month in months:
                    if(month == divisionQuery[1] ):
                        recoverMonth = months.index(month) + 1
                listOfTime.append(recoverMonth)
                break
            else:
                for month in months:
                        if(month == divisionQuery[2] ):
                            recoverMonth = months.index(month) + 1
                listOfTime.append(recoverMonth)
                break
    else:
        bool=False
        
    if(not bool):
        return listOfTime
    try:
        if(divisionQuery[2].isnumeric):
            anno = divisionQuery[2]
            listOfTime.append(int(anno))
        elif(divisionQuery[3].isnumeric):
            anno=divisionQuery[3]
            listOfTime.append(int(anno))
        else:
            anno = None
            listOfTime.append(int(anno))
    except IndexError:
        listOfTime.append(None)

    return listOfTime