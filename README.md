# Project Virgil

<p align="center">
 <img src="/asset/BannerVirgil-transformed.png" alt="Markdownify" width ="700px" >
 </p>
 

<p align="center">
  <a href="#-key-features">Key Features</a> •
  <a href="#-how-to-use">How To Use</a> •
  <a href="#-credits">Credits</a> •
  <a href="#-installing">Installing</a> •
  <a href="#-to-be-considered">To be considered!</a> 
</p>

---

Created principle with [python3.11](https://www.python.org/downloads/) e various library like [SpeechRecognition ](https://pypi.org/project/SpeechRecognition/)  and [TTS library](https://pypi.org/project/gTTS/) 

Virgil or Virgil is a virtual assistant like Alexa or Google Home, but integrated with an AI (GPT-3.5 turbo).The project is focused on the virtual assistant, but it is actually divided into two, in fact there is its own Android [app](https://github.com/Retr0100/VirgilApp) created with Flutter dedicated with which you can set, change your settings of the virtual assistant just as you would with Alexa or Google Home.


## 🔑 Key features
**You can ask lots of questions at Virgilio, like us:**
- The time ⏲️
- The weather 🌧️
- The lates news 🗞️
- Change the volume 🔉
- The temperature 🌡️
- Days of the week 📆
- Interact with the domotic (Merros device only) 💡
- Timer 🔂
- and ask **whatever you want** like: Virgilio explain quantum math 🤖
  
**Is fast to use:**
- in fact all you have to do is insert the key in the app and you're done ✅
  
**Portable:**
- You can put it on any linux/windows device including mac 🌐
  



## 📋 Installing

1. The first part of the installation is to download all the files from the repository
   - command linee ```git clone https://github.com/Retr0100/VirgilApp.git```
   - or download the zip
2. now we need the api (for now i am not rich and i do not pay for everything) so
 we are need of 4 api keys
   - API for OpenAI and GPT,
          i recommend this [video tutorial](https://www.youtube.com/watch?v=u-LeLPBZr2k) 
   - API for the weather,
          i recommend this [video tutorial](https://youtu.be/u-LeLPBZr2k?t=27) 
   - API for Merros (domotic socket),
          just create a [Merros account](https://www.meross.com/en-gc) and insert the credential
   - API for Deeple
        create an account [Deeple](https://www.deepl.com/en/docs-api/) and go on page for the API
3. When you have all the keys/accounts, save them on any file  

## 📖 How to use
### When you have installed and downloaded the API you can start using Virgilio 🥡
 1. Open a terminal to the directory ProjectVirgil/setupAndLaunch and run the file with   ```setup.bat``` for windows or run the file bash ```bash setup.sh``` on linux (first make it execuble) instead for the fast start launch   ```python launch.py``` or  ```python3 launch.py```
 2. At a certain point you will be asked to install the dedicated app [**VirgilApp**](https://github.com/Retr0100/VirgilApp), this app will allow you to configure Virgilio and change the associated settings **BUT BEWARE IT IS NOT ESSENTIAL FOR THE USE OF VIRGILIO, VIRGILIO CAN ALSO BE USED WITHOUT THE USE OF THE APP** if you do not want to use the app [click here](#-configuration-without-app) 
 3. In the app, you will have to search for the **configuration page** (it will not be difficult to find it) and you will have to enter the **key** that will be shown to you on the screen when Virgilio is launched (you only have to do this step the first time, but you can **repeat** it if you want to [change the key](#-change-the-key))
 4. Now you can change the **setting** of Virgil on the corresponding page (unfortunately, in this version of Virgilio, you must fill in all the fields and not leave any blank, otherwise Virgilio will not work properly).
 5. At the end of this initial configuration, which you only need to do once, you can press any key and choose to use a **text interface** (recommended for debugging) or a **voice interface** (recommended for personal use).

## 📃 Configuration without app

1. In the main directory there is a file call ```setting.json``` in this file is present all the setting of Virgil open it
2. Now you can modify all the setting like API key, location etc
 


## TO BE CONSIDERED ⚠️
1. The entire project is only at the albor and is not 100% complete
2. The convenience of changing settings is not the best due to the fact that if you want to change you have to re-enter all the old parameters that you do not want to change including the API keys
3. Virgilio without the API insert and without the connection will not function fully 
4. **FOR NOW** many command works only in italian except for the question at GPT (so any questions not covered by the default commands)
5. The api for GPT and Deeple is almost free but is necessary inser the credit/debit card (sorry i know is annoying) 💸


## 💎 Future idea/goal for this project

> Is improve the code and its efficiency and improve the mobile application perhaps with the possibility of changing more values and increasing the customisation of the app and Virgilio and expand the compatibily, improve Virgilio itself with perhaps the possibility of understanding other languages, adding more commands and **CREATE A PERSONAL VOICE FOR THE VIRTUAL ASSISTANT**👾

## 💸 Credits and technologies used
Only me 💻 and

 - openAI API
 - Deeple API
 - OpenMeteo API
 - Merros API
 - MongoDB for Database of the setting
 - Flask for create the API
 - Flutter for create the mobile app (only android for now)
 - Firebase for the manage of account

ps: follow me on [instagram](https://www.instagram.com/akiidjk) and [twitter](https://twitter.com/R3tr0_fj) contact me for help or support


