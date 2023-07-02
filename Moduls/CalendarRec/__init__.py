from prefix.creation import Log 
import datetime
import calendar
import calendar
import datetime
import locale

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



def recovery(stringa:str):
    if(stringa =="mi dici che giorno è"):
        giorno = datetime.datetime.today()
        lista = [giorno,None,None]
        return lista
    if(" il " in stringa):   
        stringa=stringa.split(" il ")[1].strip()
    else:
        stringa=stringa.split(" è ")[1].strip()
    division = stringa.split(" ")
    lista = []
    
    if(division[0].isnumeric()):
        giorno=division[0]
        lista.append(int(giorno))
    else:
        if(division[0] == "domani"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1) # Calcola il numero del giorno della settimana di domani
            giorno = tomorrow.day  # Converte il numero in una stringa corrispondente al giorno della settimana
            lista.append(giorno)
        elif(division[0] == "ieri"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=-1) # Calcola il numero del giorno della settimana di domani
            giorno = tomorrow.day  # Converte il numero in una stringa corrispondente al giorno della settimana
            lista.append(giorno)
        elif(division[0] == "oggi"):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=0) # Calcola il numero del giorno della settimana di domani
            giorno = tomorrow.day  # Converte il numero in una stringa corrispondente al giorno della settimana
            lista.append(giorno)
        elif((division[0] == "dopo") and (division[1] == 'domani') ):
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(days=2) # Calcola il numero del giorno della settimana di domani
                giorno = tomorrow.day  # Converte il numero in una stringa corrispondente al giorno della settimana
                lista.append(giorno)
    
    mesi=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    bool=True
    for x in mesi:
        if(x in stringa):
            if("dopo domani" not in stringa):
                for meseInd in mesi:
                    if(meseInd == division[1] ):
                        mese = mesi.index(meseInd) + 1
                lista.append(mese)
                break
            else:
                for meseInd in mesi:
                        if(meseInd == division[2] ):
                            mese = mesi.index(meseInd) + 1
                lista.append(mese)
                break
    else:
        bool=False
        
    if(not bool):
        
        return lista
    try:
        if(division[2].isnumeric):
            anno = division[2]
            lista.append(int(anno))
        elif(division[3].isnumeric):
            anno=division[3]
            lista.append(int(anno))
        else:
            anno = None
            lista.append(int(anno))
    except IndexError:
        lista.append(None)

    return lista