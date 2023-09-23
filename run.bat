@echo off
python compare_requirements.py
pip install -r requirements.txt
python main.py
pause
