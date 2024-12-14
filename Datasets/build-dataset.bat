@echo off
REM Cambia "mi_script.py" al nombre de tu script de Python
REM %1 y %2 son los parámetros para las rutas de las carpetas
python download-dataset.py "%1" "%2"
pause