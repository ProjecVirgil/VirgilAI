"""_summary_

    Returns:
        _type_: _description_
    """
import json
import re

from lib.logger import Logger


# ---- This file convert all the number in word ----

# Because the ElevenLabs TTS read the number only in english



class Utils:
    """
    _summary_
    """
    def __init__(self) -> None:
        self.logger = Logger()

    def count_number(self,command:str):
        """_summary_

        Args:
            command (str): _description_

        Returns:
            _type_: _description_
        """
        number_find = re.findall(r'\d+', command)
        return len(number_find)


    def clean_buffer(self,data_empty:dict,file_name:str):
        """_summary_

        Args:
            dataEmpty (dict): _description_
            fileName (str): _description_
        """
        with open(f"connect/{file_name}.json", 'w',encoding="utf8") as commands:
            json.dump(data_empty,commands)
        print(self.logger.log(" cleaned buffer command"), flush=True)

    def number_to_word(self,number):
        """_summary_

        Args:
            number (_type_): _description_

        Returns:
            _type_: _description_
        """
        number = int(number)
        words_up_to_vents = [
            "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", 
            "otto", "nove","dieci", "undici", "dodici", "tredici", "quattordici", 
            "quindici", "sedici", "diciassette", "diciotto", "diciannove", "venti"
        ]

        word_dozens = [
            "", "", "venti", "trenta", "quaranta", "cinquanta", 
            "sessanta", "settanta", "ottanta", "novanta"
        ]

        word_hundreds = [
            "", "cento", "duecento", "trecento", "quattrocento", 
            "cinquecento", "seicento", "settecento", "ottocento", "novecento"
        ]

        def convert_under_1000(number):
            """_summary_

            Args:
                number (_type_): _description_

            Returns:
                _type_: _description_
            """
            if 0 <= number <= 999:
                if number < 21:
                    return words_up_to_vents[number]
                if number < 100:
                    dozen = number // 10
                    unit = number % 10
                    if unit in (1, 8):
                        word_dozen = word_dozens[dozen][:-1]
                    else:
                        word_dozen = word_dozens[dozen]
                    if dozen == 1 and unit == 0:
                        return "dieci"
                    if dozen == 8 and unit == 0:
                        return "ottanta"
                    return word_dozen + words_up_to_vents[unit]

                hundred = number // 100
                remainder = number % 100
                if remainder == 0:
                    return word_hundreds[hundred]
                
                return word_hundreds[hundred] + convert_under_1000(remainder)

        if 0 <= number <= 9999:
            if number < 1000:
                return convert_under_1000(number)

            thousands = number // 1000
            remainder = number % 1000
            result = ""
            if thousands == 1:
                result += "mille"
            else:
                result += words_up_to_vents[thousands] + "mila"
            if remainder > 0:
                if remainder < 100:
                    result += "e"
                result += convert_under_1000(remainder)
            return result
        return "Unmanaged number"
