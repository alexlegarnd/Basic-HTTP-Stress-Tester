@echo off
pip install -r src\requirements.txt
pyinstaller --clean --console --icon=icon.ico -n=st src\main.py
