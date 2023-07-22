from lib.prefix import Log 
import time


def numero_in_parole(numero):
    # Definizione delle parole per i numeri da 0 a 19
    parole_fino_a_venti = [
        "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
        "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"
    ]

    # Definizione delle parole per le decine
    parole_decine = [
        "", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"
    ]

    # Gestione dei numeri fino a 99
    if 0 <= numero <= 99:
        if numero < 20:
            return parole_fino_a_venti[numero]
        else:
            decina = numero // 10
            unita = numero % 10
            # Regola di grammatica: se l'unità è 1 o 8, la decina perde l'ultima lettera
            if unita == 1 or unita == 8:
                parole_decina = parole_decine[decina][:-1]
            else:
                parole_decina = parole_decine[decina]
            return parole_decina + parole_fino_a_venti[unita]

    # Altri casi (numerazioni superiori a 99 non gestite in questo esempio)
    return "Numero non gestito"




def now():
    print(Log(" Time function"))
    named_tuple = time.localtime() # get struct_time
    ore = time.strftime('%H',named_tuple)
    minuti = time.strftime('%M',named_tuple)
    oreInParole = numero_in_parole(int(ore))
    minutiInParole = numero_in_parole(int(minuti))
    time_string = (f"Sono le {str(oreInParole)} e {str(minutiInParole)}  minuti")
    print(time.strftime("\nVirgilio: Sono le %H e %M minuti", named_tuple))
    return time_string