Created in principle with Python 3.11 e different library such us SpeechRecognition and TTS library.
Created principle with [python3.11](https://www.python.org/downloads/) e various library like [SpeechRecognition ](https://pypi.org/project/SpeechRecognition/)  and [TTS library](https://pypi.org/project/gTTS/) 

<p align="center">
 <img src="/docs/BannerVirgil-transformed.png" alt="Markdownify" width ="700px" >
</p>


Virgilio or Virgil is a virtual assistant like Alexa or Google Home, but integrated with an AI (GPT-3.5 turbo).The project is focused on the Ai/Virtual Assistant, but the idea is to develop the project in a second part, which consists of a multi-platform application created with Dart and Flask, allowing the customisation of the virtual assistant.

Key features
You can ask lots of questions at Virgilio, like us:

## Key features
You can ask lots of questions at Virgilio, like us:
- The time ⏲️
- The weather 🌧️
- The latest news 🗞️
- The lates news 🗞️
- Change the volume 🔉
- The temperature 🌡️
- Days of the week 📆
- Interact with the domotic (Merros device only) 💡
- Timer 🔂
- and ask whatever you want like: Virgilio explain quantum math 🤖

Installation

The first part of the installation is to download all the files from the repository
After that, open a terminal to the directory and run pip install -r requirements.txt
Now we need the API (for now i am not rich and i do not pay for everything) so we are need of 3 tokens
API for OpenAI and GPT API, I recommend this video tutorial
API for the weather, i recommend this video tutorial
API for Merros (domotic socket), just create a Merros account
once you have all the tokens/accounts, create a file called secret.json
and copy it by replacing the token with the your token 

secret.json

{
     "api":"sk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
     "weather":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
     "merros":["email","password"]
 }

When/if the installation is go done and you have set up the json, just run the main.py python file.
How to use it
Just run the command python main.py or python3 main.py in the terminal 📃

IMPORTANT!!
- and ask **whatever you want** like: Virgilio explain quantum math 🤖

## Installing

1. The first part of the installation is to download all the files from the repository
2. After that, open a terminal to the directory and run  ```pip install -r requirements.txt```
3. now we need the api (for now i am not rich and i do not pay for everything) so
 we are need of 3 tokens
   - API for OpenAI and GPT,
          i recommend this [video tutorial](https://www.youtube.com/watch?v=u-LeLPBZr2k) 
   - API for the weather,
          i recommend this [video tutorial](https://youtu.be/u-LeLPBZr2k?t=27) 
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

The api for GPT is almost free but is necessary inser the credit/debit card (sorry i now is annoying) 💸

Future idea/goal for this project
Is to create a multi-platform application with Dart and Flask to give the possibility to modify ALL (Word activation, position for weather and news, configure the domotic, etc..) 👾
## Future idea/goal for this project

> Is to create a multi-platform application with Dart and Flask to give the possibility to modify ALL (Word activation, position for weather and news, configure the domotic, etc..) 👾

Credits
Only me 💻
## Credits
Only me 💻 

ps: follow me on instagram and twitter contact me for help or support
ps: follow me on [instagram](https://www.instagram.com/akiidjk) and [twitter](https://twitter.com/R3tr0_fj) contact me for help or support
