@echo off

cls
echo If the next command create an error dowload python
python --version
echo Wait i am install the libray...
pip install poetry
poetry install
echo Library installation completed!
pause
cd ..
echo Running launch.py...
python launch.py


