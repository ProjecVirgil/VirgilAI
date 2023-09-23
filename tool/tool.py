import math
import speech_recognition as sr
import time
listener = sr.Recognizer()
def main(languageChoose:str):
    print("SAY A WORD OR PHRASE IN YOUR LANGAGE")
    resultDict = {}
    for i in range(5):
        try:
            with sr.Microphone() as source:
                print(f"{i}. SPEAK")
                start_time = time.time()
                voice = listener.listen(source,3,15)
                command = listener.recognize_google(voice,language=languageChoose)
                end_time = time.time()
                resultDict[i] = [listener.energy_threshold,command,end_time - start_time]
        except sr.exceptions.WaitTimeoutError:
            pass
    return resultDict
if __name__ == "__main__":
    listener.operation_timeout = 2
    listener.dynamic_energy_threshold = True
    languageChoose = str(input("Insert your language nation and dialet if is not dialet simple repeate the nation example it-it: "))
    results  = main(languageChoose)
    sorted_keys = sorted(results.keys(), key=lambda key: results[key][2])
    sorted_dict = {key: results[key] for key in sorted_keys}
    print(f"Recommended value:  {math.ceil(list(sorted_dict.values())[0][0])}")