# Virtual Environment Setup  

Este proyecto requiere configurar un entorno virtual antes de ejecutarse.  

## 1. Verificar instalación de Python  
- **Comando**: `python --version` (o `py --version`)  
- **Requisito**: Python 3.9 o superior  

## 2. Abrir carpeta del proyecto  
- **Comando**: `cd HACKATON2025`  

## 3. Crear el entorno virtual  
- **Windows**: `python -m venv .venv` (o `py -m venv .venv`)  
- **Mac / Linux**: `python3 -m venv .venv`  
- **Resultado**: Se crea la carpeta `.venv` dentro del proyecto  

## 4. Activar el entorno virtual  
- **Windows (CMD)**: `.venv\Scripts\activate`  
- **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`  
  - Si hay error de permisos:  
    `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`  
- **Mac / Linux**: `source .venv/bin/activate`  
- **Indicador**: Aparece `(.venv)` en la terminal  

## 5. Actualizar pip (opcional)  
- **Comando**: `python -m pip install --upgrade pip`  

## 6. Instalar dependencias del proyecto  
- **Comando**: `pip install -r requirements.txt`  
- **Incluye**: Django, Pillow, requests, etc.  

## 7. Colocar archivos de modelos  
- **Acción**: Poner los archivos dentro de la carpeta **Predict** (⚠️ no en *models*).  

## 8. Entrar al proyecto  
- **Comando**: `cd hackaton2025`  

## 9. Ejecutar el servidor  
- **Comando**: `python manage.py runserver`  

## 10. Acceder al host local  
- **Salida esperada**:  
  `Starting development server at http://127.0.0.1:8000/`  
- **Acción**: Abrir el enlace en el navegador  
