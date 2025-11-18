@echo off
title 2048 Game
echo Creating virtual environment...
IF NOT EXIST venv (
    python -m venv venv
)

echo Activating environment...
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Starting program...
python src/main.py

pause