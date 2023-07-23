def numberToWord(number:str):
    # Definizione delle parole per i numeri da 0 a 19
    wordsUpToVents = [
        "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
        "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove","venti"
    ]

    # Definizione delle parole per le decine
    wordDozens = [
        "", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"
    ]
    number = int(number)
    # Gestione dei numeri fino a 99
    if 0 <= number <= 99:
        if number < 21:
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