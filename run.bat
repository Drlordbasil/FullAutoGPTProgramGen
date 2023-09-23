@echo off
pip freeze > installed.txt
for /F "delims==" %%i in (installed.txt) do findstr /B /L %%i requirements.txt || pip uninstall -y %%i
del installed.txt
pip install -r requirements.txt
python MasterAI.py
pause
