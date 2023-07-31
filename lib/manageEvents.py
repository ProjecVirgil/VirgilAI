import datetime

from lib.prefix import Log
from lib.request import getEvents, createEvents


# ----- Calendar Event Function -----
class EventScheduler:
    def __init__(self):
        print(Log("fetching date"), flush=True)
        self.currentDate = datetime.datetime.now().date()
        self.formattedDate = self.currentDate.strftime("%d-%m-%Y")
        self.formattedDate = self.formattedDate.split("-")
        self.formattedDate[1] = self.formattedDate[1].replace("0", "")
        self.formattedDate = "-".join(self.formattedDate)
        print(Log("fetching events"), flush=True)
        self.events = getEvents()

    def sendNotify(self):
        try:
            todayEvents = self.events[self.formattedDate]
            phrase = "Ciao ti ricordo che oggi hai vari impegni: "
            for event in todayEvents:
                phrase = phrase + event.strip() + " "
        except:
            phrase = "Oggi non hai nessun impegno goditi la giornata"
        print(Log(f" {phrase}"), flush=True)
        return phrase

    #CREATE EVENT
    def splitTheDate(self, listOfDate:list):
        if(len(listOfDate) != 3):
            for _ in range(3-len(listOfDate)):
                    listOfDate.append(None)
            print(Log(f" result: {listOfDate}"),flush=True)
            day = listOfDate[0]
            month = listOfDate[1]
            year = listOfDate[2]
            if(month != None  and year != None ):
                return(day,month,year)
            elif(year == None and month != None):
                return(day,month,dateCurrente.year)
            else:
                return(day,self.currentDate.month,self.currentDate.year)
        else:
            print(Log(f" result: {listOfDate}"), flush=True)
            day=listOfDate[0]
            month=listOfDate[1]
            year=listOfDate[2]
            print(Log(" pre dayOfWeek function"),flush=True)
            if(month != None  and year != None ):
                return(day,month,year)
            elif(year == None and month != None):
                return(day,month,self.currentDate.year)
            else:
                return(day,self.currentDate.month,self.currentDate.year)

    def getDate(self, command:str):
        listOfTime = []
        if(" il " in command or "il " in command):
            query = command.split("il")[1].strip()
        else:
            query = ""
        splitQuery = query.split(" ")

        if(splitQuery[0].isnumeric()):
            day = splitQuery[0]
            listOfTime.append(int(day))
        else:
            if("domani" in command ):
                    tommorrow = self.currentDate.today()
                    day = tommorrow + datetime.timedelta(days=1)
                    listOfTime.append(day.day)
            elif("oggi" in command):
                    listOfTime.append(self.currentDate.day)
            elif(( "dopo" in command) and (command.split(" ")[2] == "domani") ):
                    aftertomorrow = self.currentDate.today()
                    day = aftertomorrow + datetime.timedelta(days=2)
                    listOfTime.append(day.day)

        months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
        thereAreMonth=True
        recoverMonth = ''
        for x in months:
            if(x in splitQuery):
                if("dopo domani" not in splitQuery):
                    for month in months:
                        if(month in splitQuery[1]):
                            recoverMonth = months.index(month) + 1
                    listOfTime.append(recoverMonth)
                    break
        else:
            thereAreMonth=False
        if(not thereAreMonth):
            return listOfTime
        try:
            if(splitQuery[2].isnumeric()):
                year = splitQuery[2]
                listOfTime.append(int(year))
            else:
                listOfTime.append(None)
        except IndexError:
            listOfTime.append(None)

        return listOfTime

    def recoverDate(self, command:str):
        if("che" in command):
            commandSplit = command.split(" che ")[1]
            date = self.getDate(commandSplit)
            if(len(date) != 3 or None in date):
                date = self.splitTheDate(date)
                dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
                return dateFormattedCorrectly
            else:
                dateFormattedCorrectly = f"{date[0]}-{date[1]}-{date[2]}"
                return dateFormattedCorrectly

        elif("per" in command):
            commandSplit= command.split(" per ")[1]
            date = self.getDate(commandSplit)
            if(len(date) != 3 or None in date):
                date = self.splitTheDate(date)
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