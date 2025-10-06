# Virtual Environment Setup  

This project requires setting up a virtual environment before running.  

## 1. Verify Python installation  
- **Command**: `python --version` (or `py --version`)  
- **Requirement**: Python 3.9 or higher  

## 2. Open the project folder  
- **Command**: `cd HACKATON2025`  

## 3. Create the virtual environment  
- **Windows**: `python -m venv .venv` (or `py -m venv .venv`)  
- **Mac / Linux**: `python3 -m venv .venv`  
- **Result**: Creates a `.venv` folder inside the project  

## 4. Activate the virtual environment  
- **Windows (CMD)**: `.venv\Scripts\activate`  
- **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`  
  - If you get a permissions error:  
    `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`  
- **Mac / Linux**: `source .venv/bin/activate`  
- **Indicator**: You will see `(.venv)` in the terminal  

## 5. Update pip (optional)  
- **Command**: `python -m pip install --upgrade pip`  

## 6. Install project dependencies  
- **Command**: `pip install -r requirements.txt`  
- **Includes**: Django, Pillow, requests, etc.  

## 7. Place model files  
- **Action**: Put the files inside the **Predict** folder (⚠️ not inside *models*).  
- **Action**: Put the file 'plantnet300K_metadata.json' inside the **...\cosette212.github.io-main\HACKATON2025\hackaton2025\Predict**.  

## 8. Enter the project  
- **Command**: `cd hackaton2025`  

## 9. Run the server  
- **Command**: `python manage.py runserver`  

## 10. Access the local host  
- **Expected output**:  
  `Starting development server at http://127.0.0.1:8000/`  
- **Action**: Open the link in your browser (Ctrl + Click).  
