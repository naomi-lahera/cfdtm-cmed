@echo off
REM Cambia "mi_script.py" al nombre de tu script de Python
REM %1 y %2 son los parámetros para las rutas de las carpetas
python download-dataset-selenium.py 
python extract-text.py 
python pre-build-dataset.py 
python extract-features.py 
pause