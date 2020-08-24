@echo off
pip install -r src\requirements.txt
pyinstaller --onefile --clean --console -n=st src\main.py