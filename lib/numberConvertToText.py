def numberToWord(number: str):
    # Definizione delle parole per i numeri da 0 a 19
    wordsUpToVents = [
        "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
        "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove", "venti"
    ]

    # Definizione delle parole per le decine
    wordDozens = [
        "", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"
    ]

    # Definizione delle parole per le centinaia
    wordHundreds = [
        "", "cento", "duecento", "trecento", "quattrocento", "cinquecento", "seicento", "settecento", "ottocento", "novecento"
    ]

    def convert_under_1000(number):
        if 0 <= number <= 999:
            if number < 21:
                return wordsUpToVents[number]
            elif number < 100:
                dozen = number // 10
                unit = number % 10
                # Regola di grammatica: se l'unità è 1 o 8, la decina perde l'ultima lettera
                if unit == 1 or unit == 8:
                    wordDozen = wordDozens[dozen][:-1]
                else:
                    wordDozen = wordDozens[dozen]
                if dozen == 1 and unit == 0:
                    return "dieci"
                elif dozen == 8 and unit == 0:
                    return "ottanta"
                else:
                    return wordDozen + wordsUpToVents[unit]
            else:
                hundred = number // 100
                remainder = number % 100
                if remainder == 0:
                    return wordHundreds[hundred]
                else:
                    return wordHundreds[hundred] + convert_under_1000(remainder)

    number = int(number)

    if 0 <= number <= 9999:
        if number < 1000:
            return convert_under_1000(number)
        else:
            thousands = number // 1000
            remainder = number % 1000
            result = ""
            if thousands == 1:
                result += "mille"
            else:
                result += wordsUpToVents[thousands] + "mila"
            if remainder > 0:
                if remainder < 100:
                    result += "e"
                result += convert_under_1000(remainder)
            return result

    return "Unmanaged number"