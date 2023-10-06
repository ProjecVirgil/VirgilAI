"""Tool for set the sensibility of MIC.

Returns:
      _type_: _description_
"""
import math
import speech_recognition as sr
import time

listener = sr.Recognizer()


def main(language: str):
    """Main function.

    Args:
        language (str): _description_

    Returns:
        _type_: _description_
    """
    print("SAY A WORD OR PHRASE IN YOUR LANGAGE")
    result_dict = {}
    for i in range(5):
        try:
            with sr.Microphone() as source:
                print(f"{i}. SPEAK")
                start_time = time.time()
                voice = listener.listen(source, 3, 15)
                command = listener.recognize_google(voice, language=language)
                end_time = time.time()
                result_dict[i] = [listener.energy_threshold, command, end_time - start_time]
        except sr.exceptions.WaitTimeoutError:
            pass
    return result_dict


if __name__ == "__main__":
    listener.operation_timeout = 2
    listener.dynamic_energy_threshold = True
    language_choose = str(
        input("Insert your language nation and dialet if is not dialet simple repeate the nation example it-it: "))
    results = main(language_choose)
    sorted_keys = sorted(results.keys(), key=lambda key: results[key][2])
    sorted_dict = {key: results[key] for key in sorted_keys}
    print(f"Recommended value:  {math.ceil(list(sorted_dict.values())[0][0])}")
