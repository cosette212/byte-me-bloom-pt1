Virtual Environment Setup
Follow these steps to create and activate your virtual environment before running the project. 
1️) Make sure Python is installed Check your Python version: python --version (or on some systems: py --version) It’s recommended to use Python 3.9 or higher.

2)Open the project folder: cd HACKATON2025

3)Create the virtual environment On Windows:
python -m venv .venv (if that doesn’t work, try: py -m venv .venv) 
On Mac or Linux: python3 -m venv .venv This will create a folder named .venv inside the project.

4)Activate the virtual environment 
Windows (CMD): .venv\Scripts\activate 
Windows (PowerShell): ..venv\Scripts\Activate.ps1 (If you get a permissions error, run this first: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned)

Mac / Linux: 
source .venv/bin/activate When you see something like (.venv) C:\Users\YourName\HACKATON2025>, the environment is active.

5)Update pip (optional): python -m pip install --upgrade pip

6)Install the project dependencies 
pip install -r requirements.txt 
This will download all the required libraries automatically (Django, Pillow, requests, etc).
