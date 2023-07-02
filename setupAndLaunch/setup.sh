#!/bin/bash

clear
echo "Wait, I am installing the library..."
cd ../
pip install -q -r requirements.txt
sudo apt install python3-pyaudio
echo "Library installation completed!"
echo "Press Enter to continue..."
read
echo "Running launch.py..."
python3 launch.py

