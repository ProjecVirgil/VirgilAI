# Project Virgil

<p align="center">
 <img src="/docs/Project_Virgilio (1).png" alt="Markdownify" width ="700px" >
 </p>
 

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#installing">Installing</a> •
  <a href="#important">Important!</a> 
</p>

---

Created principle with [python3.11](https://www.python.org/downloads/) e various library like [SpeechRecognition ](https://pypi.org/project/SpeechRecognition/)  and [TTS library](https://github.com/coqui-ai/TTS) 

Virgilio or Virgil is a virtual assistant like Alexa or Google Home but is integrated with an AI (GPT-3.5 turbo).The project is focused on the Ai/virtual assistant, but the idea is the evolve the project in a second part, which consists of a multi-platform app created with Dart and Flask, allowing the customisation of the virtual assistant


## Key Features
You can ask lots of questions at Dant3, like us:
- The time ⏲️
- The wheather 🌧️
- The last news 🗞️
- Change the volume 🔉
- The temperature 🌡️
- The days of the week 📆
- Interact with the domotic (only merros device) 💡
- Timer 🔂
- and ask **whatever you want** like: Virgilio explain quantum mathematics 🤖

## Installing

1. The first part of the installation is to download all the files from the repository
2. After that, open a terminal to the directory and run  ```pip install -r requirements.txt```
3. now we need the api (for now i am not rich and i do not pay for everything) so
 we are need of 3 tokens
   - API for OpenAI and GPT,
          i recommend this [video tutorial](https://videodamettere.com) 
   - API for the weather,
          i recommend this [video tutorial](https://videodamettere.com) 
   - API for Merros (domotic socket),
          just create a Merros account
4. when you have all the tokens/accounts, create a file called `secret.json`
5. and copy this by replacing the token with the your token
   secret.json
   ```
   {
        "api":"sk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "weather":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "merros":["email","password"]
    }
   ```
7. when/if the installation is go done and you have setup the json, just run the python file main.py

## How to use
> Simply run the command `python main.py` or `python3 main.py` in the terminal 📃

## IMPORTANT!!
The project is very young and is in alpha, indeed missing a good code, there are a lot of bugs or problem and the AI working principle in Italian expect for the part of AI, also the assistant is personalize only via code (for now). 🐛

There are different  path to modify and where is necesarry modify with the correct path 🛣️

- file TurnTheLight.py (Moduls,Theligh) line 10 
- file WhatsIs.py (Moduls,TheWeather) line 11
- file SendCommand.py (Moduls,ChooseCommand) line 28

The api for GPT is almost free but is necessary inser the credit/debit card (sorry i now is annoying) 💸

## Future idea/goal for this project

> Is to create a multi-platform application with Dart and Flask to give the possibility to modify ALL (Word activation, position for weather and news, configure the domotic, etc..) 👾

## Credits
Only me 💻 

ps: follow me on [instagram](https://www.instagram.com/akiidjk) and [twitter](https://twitter.com/R3tr0_fj) contact me for help or support


