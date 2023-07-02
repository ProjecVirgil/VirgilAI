@echo off

cls
echo Wait i am install the libray...
cd ..
pip install -q -r requirements.txt
echo Library installation completed!
pause
echo Running launch.py...
python launch.py


