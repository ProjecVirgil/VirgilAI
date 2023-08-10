import calendar
from datetime import datetime as datedate
import datetime


from lib.sound import Audio
from lib.logger import Logger
from lib.utils import Utils


# ---- File for get the week of the day ----
class Calendar:
    
    def __init__(self) -> None:
        self.utils =Utils()
        self.logger = Logger()
        self.audio = Audio()
        
        
    
    def indexDayOfWeek(self,year:int,month:int,day:int):
        year = int(year)
        month = int(month)  
        day = int(day)
        index= 0
        for week in calendar.monthcalendar(year,month):
            for x in week:
                if(x == day):
                    index=week.index(x)
        return index
        
    def clearNumber(self,day:str,month:str):
        day = int(day)
        month = int(month)
        day = str(day)
        month = str(month)
        return day,month
    
    def genPhrase(self,date):
        day,month,year = date.split("-")
        day,month = self.clearNumber(day,month)
        indexWeek = self.indexDayOfWeek(year,month,day)
        week = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]
        months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
        print(f"Il {day} di {months[int(month)-1]} del {year} è {week[indexWeek]}", flush=True)
    
        if((day == None or day == '' ) or month == None or year ==  None ):
            print("Mi dispiace ma non sono riuscito a capire bene la data puoi rifare la domanda",flush=True)
            self.audio.create(file=True,namefile="ErrorDate")
        else:
            if(day != 1 or day != 11):
                return f"Il {self.utils.numberToWord(str(day))} di {months[int(month)-1]} del {self.utils.numberToWord(str(year))} è {str(week[indexWeek])}"
            else:
                return f"L'{self.utils.numberToWord(str(day))} di {months[int(month)-1]} del {self.utils.numberToWord(str(year))} è {str(week[indexWeek])}"
        
        
    def recovMonth(self,query:str):
        months=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
        query = query.lower()
        for month in months:
            if(month in query):
                if(len(str(months.index(month)+1)) == 1):
                    monthReplace = "0" + str(months.index(month)+1)
                else:
                    monthReplace = str(months.index(month)+1)
                query = query.replace(month,monthReplace)
        return query
    
    def recovDate(self,query:str):
        patterns = ["%d %m %Y","%d %m","%d"]
        dateCurrent = datedate.now()
        formattedDate = dateCurrent.strftime('%d-%m-%Y') 
        query = self.recovMonth(query)
        print(query)
        for pattern in patterns:
            try:
                parsed_datetime = datedate.strptime(query, pattern)
                print(parsed_datetime)
                parsed_datetime = parsed_datetime.strftime('%d-%m-%Y')
                print(parsed_datetime) 
                if(patterns.index(pattern) == 1):
                    parsed_datetime = parsed_datetime.replace("1900",formattedDate.split("-")[2]) 
                    print(parsed_datetime,"1")
                    return parsed_datetime
                elif(patterns.index(pattern) == 2):
                    parsed_datetime = parsed_datetime.replace("01",formattedDate.split("-")[1]) 
                    parsed_datetime = parsed_datetime.replace("1900",formattedDate.split("-")[2])
                    print(parsed_datetime,"2")
                    return parsed_datetime
                else:
                    print(parsed_datetime)
                    return parsed_datetime
            except ValueError:
                pass  
    
        
    def splitCommand(self,command:str):
        try:
            if(" il " in command or "il " in command):
                query=command.split("il")[1].strip()
            elif("l'" in command or "l' " in command):
                query=command.split(" l'")[1].strip()
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
            return query
        except IndexError:
            return "ERROR"
    
    def recovPresetDate(self,command:str):
        PATTERN = "%d-%m-%Y"
        print(command)
        if(command == "che giorno e" or command == "che giorno e'"):
                todayDate  = datetime.datetime.now().date()
                formattedDate = todayDate.strftime(PATTERN)
                return formattedDate
        elif(("dopo" in command) and ("domani" in command)):
                today = datetime.datetime.today()
                afterTomorrow = today + datetime.timedelta(days=2) 
                formattedDate = afterTomorrow.strftime(PATTERN)
                return formattedDate
        elif("domani" in command):
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(days=1) 
                formattedDate = tomorrow.strftime(PATTERN)
                return formattedDate
        elif("ieri" in command):
                today = datetime.datetime.today()
                yesterday = today + datetime.timedelta(days=-1) 
                formattedDate = yesterday.strftime(PATTERN)
                return formattedDate
        elif("oggi" in command):
                today = datetime.datetime.today()
                today = today + datetime.timedelta(days=0) 
                formattedDate = today.strftime(PATTERN)
                return formattedDate
        else:
            return None

        
    def getDate(self,command:str):
        presetDate  = self.recovPresetDate(command)
        print(presetDate)
        if(presetDate == None):
            commandSplitted = self.splitCommand(command)
            date = self.recovDate(commandSplitted)
            output = self.genPhrase(date)
            return output
        else:
            output = self.genPhrase(presetDate)
            return output
    
    def getDiff(self,command:str):
        date  = self.recovPresetDate(command)
        if(date == None):
            commandSplitted = self.splitCommand(command)
            date = self.recovDate(commandSplitted)
        day,month,year = date.split("-")
        day,month = self.clearNumber(day,month)
        correct_date = datetime.datetime(int(year), int(month), int(day))
        diff_days = (datetime.datetime.now() - correct_date).days
        print(self.logger.Log(f"result: Al {day} {month} {year} mancano {diff_days * -1}"), flush=True)
        if(diff_days * -1 == 1):
            return f" Al {self.utils.numberToWord(day)} {self.utils.numberToWord(month)} {self.utils.numberToWord(year)} manca un giorno"
        else:
            return f" Al {self.utils.numberToWord(day)}, {self.utils.numberToWord(month)}, {self.utils.numberToWord(year)} mancano {self.utils.numberToWord(diff_days * -1)} giorni"
        
        
