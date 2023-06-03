from prefix.creation import Log 
import datetime
import calendar

def day(giorno:str,mese:int = None, anno:int = None):
    print(Log(" DayOfWeek function"))
    data_corrente = datetime.datetime.now()
    if(mese == None):
        mese = data_corrente.month
    if(anno ==None):
        anno = data_corrente.year
    for settimana in calendar.monthcalendar(anno,mese):
        for x in settimana:
            if( x == giorno):
                dayOfWeek=settimana.index(x)

    settimana = ["Lunedi","Martedi","Mercoledi","Giovedi","Venerdi","Sabato","Domenica"]
    stringa = f"Il {giorno} di {mese} del {anno} è {settimana[dayOfWeek]}"
    print(f"Il {giorno} di {mese} del {anno} è {settimana[dayOfWeek]}")
    return stringa