from prefix.creation import Log

def change(command:str):
    print(Log(" volume function"))
    comando=command.split(" ")
    volume = comando[-1]
    if(("." in volume) and ("%" in volume)):
        volume= volume[:-2]
    elif(("%" in volume) or ("." in volume)):
        volume = volume[:-1]
    volume = int(volume)/100
    if(volume < 0.1 ):
        return 104
    else:
        return volume