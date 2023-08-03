import datetime

from lib.logger import Logger   
from lib.request import MakeRequests 
from lib.calendarRec import Calendar

# ----- Calendar Event Function -----
class EventScheduler:
    
    def __init__(self):
        self.logger = Logger()
        self.request_maker = MakeRequests()
        self.calendar = Calendar()
        
        print(self.logger.Log("fetching date"), flush=True)
        self.currentDate = datetime.datetime.now().date()
        self.formattedDate = self.currentDate.strftime("%d-%m-%Y")
        self.formattedDate = self.formattedDate.split("-")
        self.formattedDate[1] = self.formattedDate[1].replace("0", "")
        self.formattedDate = "-".join(self.formattedDate)
        print(self.logger.Log("fetching events"), flush=True)
        
        
    def sendNotify(self):
        try:
            todayEvents = self.events[self.formattedDate]
            phrase = "Ciao ti ricordo che oggi hai vari impegni: "
            for event in todayEvents:
                phrase = phrase + event.strip() + " "
        except:
            phrase = "Oggi non hai nessun impegno goditi la giornata"
        print(self.logger.Log(f" {phrase}"), flush=True)
        return phrase


    def getDate(self,command):
        presetDate  = self.calendar.recovPresetDate(command)
        print(presetDate)
        if(presetDate == None):
            commandSplitted = self.calendar.splitCommand(command)
            date = self.calendar.recovDate(commandSplitted)
            day,month,year = date.split("-")
            day,month = self.calendar.clearNumber(day,month)
            date = "-".join([day,month,year])
            return date
        else:
            return date
        

    def addEvents(self,command:str):
        print(self.logger.Log(" i will create event"),flush=True)
        if("che" in command):
            commandSplit = command.split(" che ")[1]
            date = self.getDate(commandSplit)
        elif("per" in command):
            commandSplit = command.split(" per ")[1]
            date = self.getDate(commandSplit)
        print(self.logger.Log(" i recov the date"),flush=True)
        event = command.split("ho")[1]
        print(self.logger.Log(" send the request"),flush=True)
        MakeRequests.createEvents(event,date)
        return "Promemoria creato con successo"