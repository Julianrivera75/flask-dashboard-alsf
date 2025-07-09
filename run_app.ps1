# Script para automatizar la ejecución del proyecto Python
# Guarda este archivo como run_app.ps1 y ejecútalo en PowerShell

# Navega a la carpeta del script
Set-Location -Path $PSScriptRoot

# Instala las dependencias
Write-Host "Instalando dependencias..."
pip install -r requirements.txt

# Verifica si existe credentials.json
if (!(Test-Path "credentials.json")) {
    Write-Host "ERROR: No se encontró 'credentials.json'. Por favor, copia tu archivo de credenciales reales aquí."
    exit 1
}

# Intenta ejecutar app.py, si falla intenta app_oop.py
Write-Host "Ejecutando la aplicación..."
if (Test-Path "app.py") {
    try {
        python app.py
        exit 0
    } catch {
        Write-Host "Fallo al ejecutar app.py, intentando app_oop.py..."
    }
}
if (Test-Path "app_oop.py") {
    python app_oop.py
} else {
    Write-Host "No se encontró ni app.py ni app_oop.py."
    exit 1
} 