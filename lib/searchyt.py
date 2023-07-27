import webbrowser as web
import requests



def getTopic(command:str):
    print(command.split("riproduci "))
    if("play" in command):
        topic = command.split("play ")[1]
    if("riproduci" in command):
        topic = command.split("riproduci ")[1]
    return topic


def playonyt(command: str) -> str:
        topic = getTopic(command)
        print(topic)
        url = f"https://www.youtube.com/results?q={topic}"
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count += 1
            if i == "WEB_PAGE_TYPE_WATCH":
                break
        if lst[count - 5] == "/results":
            raise Exception("No Video Found for this Topic!")
        web.open(f"https://www.youtube.com{lst[count - 5]}")
        return f"https://www.youtube.com{lst[count - 5]}"
    
