@echo off
py -3.11 -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
pause