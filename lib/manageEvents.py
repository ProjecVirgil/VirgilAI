import datetime

from lib.prefix import Log
from lib.request import getEvents,createEvents


# ----- Calendar Event Function -----

def sendNotify():    
    print(Log(" I take the date"),flush=True)
    currentDate = datetime.datetime.now().date()
    dateFormatted = currentDate.strftime("%d-%m-%Y")
    dateFormatted = dateFormatted.split("-")
    dateFormatted[1] = dateFormatted[1].replace("0","")
    dateFormatted  = "-".join(dateFormatted)
    
    print(Log(" get the events"),flush=True)
    events = getEvents()
    try:
        todayEvents = events[dateFormatted]
        phrase = "Ciao ti ricordo che oggi hai vari impegni: "
        for event in todayEvents:
            phrase = phrase + event.strip() + " "
    except:
        phrase = "Oggi non hai nessun impegno goditi la giornata"
    print(Log(f" {phrase}"),flush=True)
    return phrase

#CREATE EVENT
def splitTheDate(listOfDate:list):
    if(len(listOfDate) != 3):
        for _ in range(3-len(listOfDate)):
                listOfDate.append(None)
        print(Log(f" result: {listOfDate}"),flush=True)  
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
        print(Log(f" result: {listOfDate}"), flush=True) 
        dateCurrente = datetime.datetime.now()
        day=listOfDate[0]
        month=listOfDate[1]
        year=listOfDate[2]
        print(Log(" pre dayOfWeek function"),flush=True)
        if(month != None  and year != None ):
            return(day,month,year)
        elif(year == None and month != None):
            return(day,month,dateCurrente.year)
        else:
            return(day,dateCurrente.month,dateCurrente.year)

def getDate(command:str):
    listOfTime = []    
    if(" il " in command or "il " in command):   
        query=command.split("il")[1].strip()
    else:
        query = ""
    divisionQuery = query.split(" ")
    
    if(divisionQuery[0].isnumeric()):
        day=divisionQuery[0]
        listOfTime.append(int(day))
    else:
        if("domani" in command ):
                tommorow = datetime.datetime.today()
                day = tommorow + datetime.timedelta(days=1) 
                listOfTime.append(day.day)
        elif("oggi" in command):
                today = datetime.datetime.today()
                day = today + datetime.timedelta(days=0) 
                listOfTime.append(day.day)
        elif(( "dopo" in command) and (command.split(" ")[2] == "domani") ):
                    aftertomorrow = datetime.datetime.today()
                    day = aftertomorrow + datetime.timedelta(days=2) 
                    listOfTime.append(day.day)
                    
    months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    thereAreMonth=True
    recoverMonth = ''
    for x in months:
        if(x in divisionQuery):
            if("dopo domani" not in divisionQuery):
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
            year = divisionQuery[2]
            listOfTime.append(int(year))
        else:
            listOfTime.append(None)
    except IndexError:
        listOfTime.append(None)

    return listOfTime         
    
def recoverDate(command:str):
    if("che" in command):
        commandSplitted = command.split(" che ")[1]
        date = getDate(commandSplitted)
        if(len(date) != 3 or None in date):
            date = splitTheDate(date)
            dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
            return dateFormattedCorrectly
        else:
            dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
            return dateFormattedCorrectly
        
    elif("per" in command):
        commandSplitted= command.split(" per ")[1]
        date = getDate(commandSplitted)
        if(len(date) != 3 or None in date):
            date = splitTheDate(date)
            dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
            return dateFormattedCorrectly
        else:
            dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
            return dateFormattedCorrectly

# Main function
def addEvents(command:str):
    print(Log(" i will create event"),flush=True)
    date = recoverDate(command)
    print(Log(" i recov the date"),flush=True)
    event = command.split("ho")[1]
    print(Log(" send the request"),flush=True)
    createEvents(event,date)
    return "Promemoria creato con successo"