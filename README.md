# Virgil AI 🏛️ (Assistant Interface)  | Last docs update: 03/01/2024 (d/m/y)

## Index 📖

- **[Introduction](#introduction)**
- **[How Virgil Works](#-how-virgilai-works)**
- **[Installation](#installation)**
  - [ElevenLabs](#guide-to-elevenlabs)
- **[First start](#first-start)**
  - [How to use](#how-to-use)
- **[Problem with mic?](#%EF%B8%8F-guide-to-microphones)**
- **[Why all this key?](#why-the-key-of-openai-elevenlabs-and-merros)**
  - [Generate other key](#-change-the-key)
- **[Security](#security)**
- **[Notes](#notes-and-updates)**
- **[Other](#other)**
  - [App](#mobile-app)
  - [Websites](#website)
  - [Virgil Installer](#virgil-installer)
- **[Credits](#credits)**
  - [Contact me](#contact-me)

---

![VirgilAI](https://img.shields.io/badge/2%2C1k-2%2C1k?style=for-the-badge&logo=visualstudiocode&label=Lines%20of%20code&labelColor=282a3&color=%23164773)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/Retr0100/VirgilAI?style=for-the-badge&logo=github&labelColor=%23282a3&color=%231B7F79)
![GitHub repo size](https://img.shields.io/github/repo-size/Retr0100/VirgilAI?style=for-the-badge&logo=github&labelColor=%23282a3&color=%23bd93f9)
[![Scrutinizer Code Quality](https://img.shields.io/badge/9,6-9,6?style=for-the-badge&logo=scrutinizerci&label=Scrutinizer&labelColor=282a3&color=%23008000)](https://scrutinizer-ci.com/g/Retr0100/VirgilAI/?branch=master)

## Introduction

Created in principle with [python3.11](https://www.python.org/downloads/) and various libraries such as [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) and [TTS library](https://pypi.org/project/gTTS/).

Virgilo or Virgil is a virtual assistant like Alexa or Google Home, but integrated with an AI (powered by openai).Designed to give the user the ability to use it and do what they want with it, from putting it on a rasperry and using it as alexa to integrating it with their device whether it's linux or windows. With the possibility to set your own settings according to your needs, from where and when you want.

### 🔑 Key features

**You can ask many questions on Virgilio, like us:**.

- The time ⏲️
- The weather 🌧️
- The latest news 🗞️
- Change the volume 🔉
- The temperature 🌡️
- Days of the week 📆
- Interact with the domotic (Merros device only) 💡
- Timer 🔂
- Ask a Virgil to remember your commitments 🗓️
- Media player 🎵
- and ask **whatever you want** how: Virgilio explain quantum math 🤖
  
**Is fast to use:**

- In fact, all you have to do is insert the key into the app and you're done ✅
  
**Portable:**

- You can use it on any linux/windows 🌐

## 💻 How VirgilAI works

**white text**

### Example of communication with API and APP

<p align="center">
 <img src="assets/img/exampleVirgil.svg" alt="Markdownify" width ="80%" >
</p>

### Structure of Virgil

<p align="center">
 <img src="assets/img/HowVirgilWorks.svg" alt="Markdownify" width ="80%" >
</p>

## 📋 Installation

### Obligatory requirements

- Python 3.11
- Key from GPT3.5>=

## Installation

1. The first part of the installation is to **get** the installer with this [link](https://github.com/ProjecVirgil/VirgilInstaller/releases/) and follow the instructions (it will be easy, don't worry and ***remember to save the key***).

2. Install the [App](https://github.com/ProjecVirgil/VirgilApp) to configure your Virgil.

3. Now we need the **api** (for now I am not rich and do not pay for everything) so
 we need 3 api keys (the keys marked with * ** are mandatory for operation)
   - API for OpenAI and GPT,
          I recommend this [video tutorial](https://www.youtube.com/watch?v=u-LeLPBZr2k).
   - API for Merros (domotic socket),
          just create a [Merros account](https://www.meross.com/en-gc) and enter your credentials (key not obligatory as Merros function is disabled)
   - API for ElevenLabs
       This API is not required, but if you want a [BEST EXPERIENCE](https://elevenlabs.io/speech-synthesis) I recommend you to get it.

1. When you have all the keys/accounts, save them to any file.

### Guide to ElevenLabs

Elevenlabs is a service to reproduce tts by deeplearning and the key is free but is necessary an account but the tokens are very few...
**But is there a trick to have **UNLIMITED** accounts with the same email**

**Explanation:**

  1. Take any gmail
  2. Add a dot anywhere in the email
  3. And the confirmation email will be sent

**Example:**

Original email: `example@gmail.com`.
Email with dots added: `example.@gmail.com` or `e.xample@gmail.com`.

## First start

The first time you start Virgil immediately after booting, it will be much slower than a normal start. This is because Python, and Virgil in general, is **optimized** so that the more starts it has in a session, the faster it will start.

### How to use

## 🎙️ Guide to microphones

### **Problem**

**The recognizer tries to recognize speech even when I'm not speaking, or after I've finished speaking.**

### Solution

Try increasing the recognizer_instance.energy_threshold property. This is basically how sensitive the recognizer is to when recognition should start. Higher values mean it will be less sensitive, which is useful if you are in a loud room.

I made this tool for you (the tool is in the repository) 💓

``` python
import math
import speech_recognition as sr
import time
listener = sr.Recognizer()
def main(languageChoose:str):
    print("SAY A WORD OR PHRASE IN YOUR LANGUAGE")
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
        except:
            pass
    return resultDict
if __name__ == "__main__":
    listener.operation_timeout = 2
    listener.dynamic_energy_threshold = True
    languageChoose = str(input("Insert your language nation and dialect if is not dialect simple repeat the nation example it-it: "))
    results  = main(languageChoose)
    sorted_keys = sorted(results.keys(), key=lambda key: results[key][2])
    sorted_dict = {key: results[key] for key in sorted_keys}
    print(f"Recommended value:  {math.ceil(list(sorted_dict.values())[0][0])}")
```

The tool is not **100%** accurate, but it's a good way to get a **starting** idea if you see that Virgil is not accurate enough in recognizing when you speak and when you don't try to adjust.

### Why the key of OpenAI, ElevenLabs and Merros❓

- **Virgil**: The Virgilio configuration key is used to synchronize all online settings...  **DO NOT GIVE THE KEY TO ANYONE OR EXPORT IT TO ANYONE OR YOU WILL GET ALL YOUR KEYS** (OpenAI,Elevenlabs etc)
- **OpenAI**: This is actually the only mandatory key, as GPT covers 50% of the application, and this is the real **difference** to Alexa and Virgil.
- **ElevenLabs**: This key is not mandatory, but it makes the experience more pleasant because ElevenLabs implements a more natural Speech To Text (TTS) and also allows you to choose your own voice. If you can't use the button, Virgil will still work, but with Google's TTS.
 and it's not the best choice 😅.
- **Meross**: This is **ONLY** required if you can use a domotic Meross, but if you don't have a domotic Meross, don't waste your time ⏲️

### How to change the voice for TTS ElevenLabs

1. Go to this file ```lib/packages_utility/sound.py```
2. Go to the [ElevenLabs](https://elevenlabs.io/speech-synthesis) website and create an account (you should already have one)
3. Explore the default voice and choose one
4. Now go to this part of the ``sound.py`` file

    ```python
    sound = generate(
                      api_key = self.API_KEY,
                      text=text,
                      voice="Antoni",
                      model='eleven_multilingual_v1'
                    )
    ```

    And replace the voice with the one you want (if after the TTS does not work try another voice on watch a video on YT on how to use default entries).
  
5. Restart Virgil.


**WARNING!!:** To save ElevenLabs tokens and increase efficiency, many phrases are pre-recorded, so there will be a difference between the voice you type and the pre-recorded voice.

### 🔁 Change the key

> For change the key you can re-run the installer and modify the parameter of key in the menu

## Security

This is not a topic we will be exploring in depth at the moment, but each key is managed in a hosting system that encrypts communications and uses various string sanitization and controls against ddos and other attacks, but I believe that security can never be too much, so...
If you discover a vulnerability in Virgil, please email <projectvirgilai@gmail.com>. All vulnerabilities are reported immediately.

## Notes and Updates

### In this paragraph I will add secondary items or updates released

- The **CATONE UPDATE** is here and brings many new features

## Other

As mentioned above, VirgililAI is part of a larger project that includes an app, a website and others, the links of which are at Project:

### [Website](https://projectvirgil.net)

### [Mobile APP](https://github.com/Retr0100/VirgilApp)

### [Virgil Installer](https://github.com/Retr0100/VirgilInstaller)

## Credits

The project is made by one person and is still in development, I'm looking for someone to give me advice and a hand to continue the project, which I believe is an excellent open source and free alternative to devices like Alexa or Google Home.

### Contact me

For code related issues you can use github directly for other collaborations or alerts write to this email <projectvirgilai@gmail.com>

If you want to support a small developer take a [**special link**](https://www.paypal.me/Retr0jk) (pls i need coffee)

<div style="display: inline_block"><br>
<a href="https://www.paypal.com/paypalme/Retr0jk">
  <img width = 200 align="center" src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white" />
</a>
<a href="https://www.buymeacoffee.com/dragonfaivk"><img align="center" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" width="150"/></a>
</div>

### License

- AGPL-3.0 license
- [LICENSE FILE](https://github.com/Retr0100/VirgilAI/blob/master/LICENSE)
