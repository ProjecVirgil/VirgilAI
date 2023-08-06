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
        
        self.currentDate = datetime.datetime.now().date()
        self.formattedDate = self.currentDate.strftime("%d-%m-%Y")
        self.formattedDate = self.formattedDate.split("-")
        self.formattedDate[1] = self.formattedDate[1].replace("0", "")
        self.formattedDate = "-".join(self.formattedDate)
        
        
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
            try:
                day,month,year = date.split("-")
            except:
                day,month,year = date.split(" ")
            day,month = self.calendar.clearNumber(day,month)
            date = "-".join([day,month,year])
            return date
        else:
            return presetDate
        

    def addEvents(self,command:str):
        print(self.logger.Log(" i will create event"),flush=True)
        date,event = command.split("ho")
        if("che" in command):
            dateSplited = date.split(" che ")[1]
            date = self.getDate(dateSplited)
        elif("per" in command):
            dateSplited = date.split(" per ")[1]
            date = self.getDate(dateSplited)
        print(self.logger.Log(" i recov the date"),flush=True)
        print(self.logger.Log(" send the request"),flush=True)
        self.request_maker.createEvents(event,date)
        return "Promemoria creato con successo"