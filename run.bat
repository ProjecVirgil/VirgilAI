@echo off


echo START CHECK THE LIBRARY
pip install -q -r requirements.txt > logpip.txt
echo LIBRARY INSTALLED CORRECTLY IN CASE OF PROBLEMS, CHECK THE logpip.txt FILE
echo START THE PYTHON FILE
start python -i speechPy.py
start python -i process.py
start python -i exc.py
pause