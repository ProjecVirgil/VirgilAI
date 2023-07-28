import datetime

from lib.prefix import Log
from lib.request import getEvents,createEvents




def sendNotify():
    date = datetime.datetime.now().date()
    currentDate = date.strftime("%d-%m-%Y")
    currentDate = currentDate.split("-")
    currentDate[1] = currentDate[1].replace("0","")
    currentDate  = "-".join(currentDate)
    events = getEvents()
    todayEvents = events[currentDate]
    phrase = "Ciao ti ricordo che oggi hai vari impegni: "
    for event in todayEvents:
        phrase = phrase + event.strip() + " "
    print(phrase)
    return phrase





#CREATE EVENT
def splitTheDate(listOfDate:list):
    if(len(listOfDate) != 3):
        for _ in range(3-len(listOfDate)):
                listOfDate.append(None)
        print(Log(f" result: {listOfDate}"))  
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        dateCurrente = datetime.datetime.now()
        if(month != None  and year != None ):
            return(day,month,year)
        elif(year == None and month != None):
            return(day,month,dateCurrente.year)
        else:
            return(day,dateCurrente.month,dateCurrente.year)
    else:
        print(Log(f" result: {listOfDate}")) 
        dateCurrente = datetime.datetime.now()
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        print(day,month,year)
        print(Log(" pre dayOfWeek function"))
        if(month != None  and year != None ):
            return(day,month,year)
        elif(year == None and month != None):
            return(day,month,dateCurrente.year)
        else:
            return(day,dateCurrente.month,dateCurrente.year)


def getDate(divisionQuery:str):
    listOfTime = []    
    if(" il " in divisionQuery or "il " in divisionQuery):   
        query=divisionQuery.split("il")[1].strip()
    else:
        query = ""
    division = query.split(" ")
    
    if(division[0].isnumeric()):
        day=division[0]
        listOfTime.append(int(day))
    else:
        if("domani" in divisionQuery ):
                today = datetime.datetime.today()
                day = today + datetime.timedelta(days=1) 
                listOfTime.append(day.day)
        elif("oggi" in divisionQuery):
                today = datetime.datetime.today()
                day = today + datetime.timedelta(days=0) 
                listOfTime.append(day.day)
        elif(( "dopo" in divisionQuery) and (divisionQuery.split(" ")[2] == "domani") ):
                    today = datetime.datetime.today()
                    day = today + datetime.timedelta(days=2) 
                    listOfTime.append(day.day)
                    
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    thereAreMonth=True
    recoverMonth = ''
    for x in months:
        if(x in division):
            if("dopo domani" not in division):
                for month in months:
                    if(month in division[1]):
                        recoverMonth = months.index(month) + 1
                listOfTime.append(recoverMonth)
                break
    else:
        thereAreMonth=False
    if(not thereAreMonth):
        return listOfTime
    try:
        if(division[2].isnumeric()):
            anno = division[2]
            listOfTime.append(int(anno))
        else:
            listOfTime.append(None)
    except IndexError:
        listOfTime.append(None)

    return listOfTime         
    
def recoverDate(command):
    if("che" in command):
        commandSplitted = command.split(" che ")[1]
        data = getDate(commandSplitted)
        if(len(data) != 3 or None in data):
            data = splitTheDate(data)
            dataForQuery = f"{data[0]}-{data[1]}-{data[2]}"
            return dataForQuery
        else:
            dataForQuery = f"{data[0]}-{data[1]}-{data[2]}"
            return dataForQuery
        
    elif("per" in command):
        commandSplitted= command.split(" per ")[1]
        data = getDate(commandSplitted)
        if(len(data) != 3 or None in data):
            data = splitTheDate(data)
            dataForQuery = f"{data[0]}-{data[1]}-{data[2]}"
            return dataForQuery
        else:
            dataForQuery = f"{data[0]}-{data[1]}-{data[2]}"
            return dataForQuery

def addEvents(command:str):
    print(Log(" i will create event"))
    date = recoverDate(command)
    print(Log(" i recov the date"))
    event = command.split("ho")[1]
    print(Log(" send the request"))
    createEvents(event,date)
    return "Promemoria creato con successo"