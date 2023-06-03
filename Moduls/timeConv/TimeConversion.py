from prefix.creation import Log 

def conversion(stringa:str):
    print(Log(" Conversione in corso"))
    stringa=stringa.replace(",","")
    stringa=stringa.split(" ")
    
    if((("ora" in stringa) or ("ore" in stringa)) and (("minuto" in stringa) or ("minuti" in stringa)) and (("secondo" in stringa) or ("secondi" in stringa)) ):
        ore=int(stringa[0])
        minuti = int(stringa[2])
        secondi = int(stringa[5])
        sommaSecondi= ore*3600 + minuti * 60 + secondi
        return sommaSecondi
        
    elif((("ora" in stringa) or ("ore" in stringa)) and (("minuto" in stringa) or ("minuti" in stringa))):
        
        ore=int(stringa[0])
        minuti = int(stringa[3])
        sommaSecondi= ore*3600 + minuti * 60
        return sommaSecondi
    
    elif((("minuto" in stringa) or ("minuti" in stringa)) and (("secondo" in stringa) or ("secondi" in stringa))):
        
        minuti=int(stringa[0])
        secondi = int(stringa[3])
        sommaSecondi= minuti * 60 + secondi
        return sommaSecondi
    
    elif((("ora" in stringa) or ("ore" in stringa)) and (("secondo" in stringa) or ("secondi" in stringa))):
        
        ore=int(stringa[0])
        secondi = int(stringa[3])
        sommaSecondi= ore * 3600 + secondi
        return sommaSecondi
    
    else:
        if(((stringa[1] == 'ore')) or (stringa[1] == 'ora')):
            return int(stringa[0])*3600
        elif((stringa[1] == 'minuti') or (stringa[1] == 'minuto')):
            return int(stringa[0])*60
        else:
            return int(stringa[0])



