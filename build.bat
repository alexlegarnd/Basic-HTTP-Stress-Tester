@echo off
pip install -r src\requirements.txt
pyinstaller --clean --console -n=st src\main.py
