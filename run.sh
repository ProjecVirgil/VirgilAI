#!/bin/bash

clear
echo "Wait, I am installing the library..."
pip install -q -r requirements.txt
sudo apt install python3-pyaudio
echo "Library installation completed!"
echo "Running main.py..."
python3 main.py
echo "Press Enter to continue..."
read
