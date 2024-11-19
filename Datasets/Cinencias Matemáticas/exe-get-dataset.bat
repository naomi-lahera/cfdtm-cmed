@echo off
@REM REM Obtener la ruta absoluta del directorio donde se ejecuta el archivo .bat
@REM set "abs_path=%~dp0"

@REM REM Definir la ruta del archivo JSON y el script Python usando la ruta absoluta
@REM set "config_file=%abs_path%config.json"
@REM set "python_file=%abs_path%src\dataset.py"

@REM REM Mostrar las rutas obtenidas (opcional para depuración)
@REM echo config path: %config_file%
@REM echo file: %python_file%
@REM echo wait...

REM Ejecutar el script de Python con el archivo JSON como argumento
python "%python_file%" "%config_file%"

REM Mantener la consola abierta hasta que el usuario la cierre manualmente
echo.
echo Presiona cualquier tecla para cerrar la ventana...
pause >nul
