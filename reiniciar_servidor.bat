@echo off
echo ========================================
echo REINICIANDO SERVIDOR FLASK
echo ========================================
echo.
echo Deteniendo procesos de Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Limpiando cache de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.
echo Iniciando servidor...
python start_server.py
pause

