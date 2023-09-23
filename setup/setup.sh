#!/bin/bash

clear
echo "Wait, I am installing python.."
sudo apt install python3
sudo apt install python3-pip
python3 --version
echo "Wait, I am installing the library..."
pip install poetry
poetry install
sudo apt install python3-pyaudio
sudo apt install ffmpeg
echo "Library installation completed!"
echo "Press Enter to continue..."
read
cd ../
echo "Running launch.py..."
python3 launch.py

