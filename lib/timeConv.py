from lib.prefix import Log 

def conversion(command:str):
    print(Log(" Conversione in corso"))
    command=command.replace(",","")
    command=command.split(" ")
    
    if((("ora" in command) or ("ore" in command)) and (("minuto" in command) or ("minuti" in command)) and (("secondo" in command) or ("secondi" in command)) ):
        hours=int(command[0])
        minutes = int(command[2])
        seconds = int(command[5])
        sumSeconds= hours*3600 + minutes * 60 + seconds
        return sumSeconds
        
    elif((("ora" in command) or ("ore" in command)) and (("minuto" in command) or ("minuti" in command))):
        hours=int(command[0])
        minutes = int(command[3])
        sumSeconds= hours*3600 + minutes * 60
        return sumSeconds
    
    elif((("minuto" in command) or ("minuti" in command)) and (("secondo" in command) or ("secondi" in command))):
        minutes=int(command[0])
        seconds = int(command[3])
        sumSeconds= minutes * 60 + seconds
        return sumSeconds
    
    elif((("ora" in command) or ("ore" in command)) and (("secondo" in command) or ("secondi" in command))):
        hours=int(command[0])
        seconds = int(command[3])
        sumSeconds= hours * 3600 + seconds
        return sumSeconds
    
    else:
        if(((command[1] == 'ore')) or (command[1] == 'ora')):
            return int(command[0])*3600
        elif((command[1] == 'minuti') or (command[1] == 'minuto')):
            return str(command[0])*60
        else:
            return str(command[0])



