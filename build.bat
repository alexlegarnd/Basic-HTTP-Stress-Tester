@echo off
pip install -r src\requirements.txt
python -m PyInstaller --clean --console --icon=icon.ico -n=st src\main.py
