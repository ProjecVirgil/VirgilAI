from lib.prefix import Log 
import time

def now():
    print(Log(" Time function"))
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("Sono le %H e %M minuti", named_tuple)
    print(time.strftime("\nDante: Sono le %H e %M minuti", named_tuple))
    return time_string