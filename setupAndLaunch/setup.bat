@echo off

cls
echo If the next command create an error dowload python
python --version
echo Wait i am install the libray...
pip install -q -r requirements.txt
echo Library installation completed!
pause
echo Running launch.py...
python launch.py


