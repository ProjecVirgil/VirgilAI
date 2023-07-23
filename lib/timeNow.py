from lib.prefix import Log 
import time


def numberToWord(number):
    # Definizione delle parole per i numeri da 0 a 19
    wordsUpToVents = [
        "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
        "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"
    ]

    # Definizione delle parole per le decine
    wordDozens = [
        "", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"
    ]

    # Gestione dei numeri fino a 99
    if 0 <= number <= 99:
        if number < 20:
            return wordsUpToVents[number]
        else:
            dozen = number // 10
            unit = number % 10
            # Regola di grammatica: se l'unità è 1 o 8, la decina perde l'ultima lettera
            if unit == 1 or unit == 8:
                wordDozen = wordDozens[dozen][:-1]
            else:
                wordDozen = wordDozens[dozen]
            return wordDozen + wordsUpToVents[unit]

    return "Unmanaged number"




def now():
    print(Log(" Time function"))
    timeTuple = time.localtime() # get struct_time
    hours = time.strftime('%H',timeTuple)
    minuts = time.strftime('%M',timeTuple)
    hoursToWords = numberToWord(int(hours))
    minutsToWords = numberToWord(int(minuts))
    timeString = (f"Sono le {str(hoursToWords)} e {str(minutsToWords)}  minuti")
    print(time.strftime("\nVirgilio: Sono le %H e %M minuti", timeTuple))
    return timeString