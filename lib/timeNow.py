from lib.prefix import Log
from lib.numberConvertToText import numberToWord 
import time







def now():
    print(Log(" Time function"))
    timeTuple = time.localtime() # get struct_time
    hours = time.strftime('%H',timeTuple)
    minuts = time.strftime('%M',timeTuple)
    hoursToWords = numberToWord(hours)
    minutsToWords = numberToWord(minuts)
    timeString = (f"Sono le {str(hoursToWords)} e {str(minutsToWords)}  minuti")
    print(time.strftime("\nVirgilio: Sono le %H e %M minuti", timeTuple))
    return timeString