@echo off

REM Step 1: Clean up the environment
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q env
rmdir /s /q dist

REM Step 2: Install the required packages using Poetry
poetry install

REM Step 2.1: Install PyInstaller using pip
poetry run pip install pyinstaller

REM Step 2.2: Poetry build
poetry build

REM Step 3: Execute PyInstaller within the virtual environment
poetry run pyinstaller ./dev_assistant_client/dev_assistant_client.py --name dev-assistant --onefile --noconfirm --clean --icon=./icon.ico
