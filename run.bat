@echo off
pip freeze > installed.txt
for /F "delims==" %%i in (installed.txt) do pip uninstall -y %%i
del installed.txt
pip install -r requirements.txt
python main.py
pause
