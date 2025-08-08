# Script de PowerShell para desplegar la aplicación Flask a Railway

Write-Host "🚀 Iniciando despliegue a Railway..." -ForegroundColor Green

# Verificar que Railway CLI esté instalado
try {
    $null = Get-Command railway -ErrorAction Stop
    Write-Host "✅ Railway CLI está instalado" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI no está instalado. Instalando..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Verificar que estemos en el directorio correcto
if (-not (Test-Path "wsgi.py")) {
    Write-Host "❌ Error: No se encontró wsgi.py. Asegúrate de estar en el directorio correcto." -ForegroundColor Red
    exit 1
}

# Verificar que los archivos necesarios existan
Write-Host "📋 Verificando archivos necesarios..." -ForegroundColor Cyan
$required_files = @("Dockerfile.flask", "railway.json", "requirements.txt", "wsgi.py", "app_modular.py")
foreach ($file in $required_files) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Error: No se encontró $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Todos los archivos necesarios están presentes" -ForegroundColor Green

# Iniciar sesión en Railway (si no está ya logueado)
Write-Host "🔐 Verificando sesión de Railway..." -ForegroundColor Cyan
railway login

# Desplegar a Railway
Write-Host "🚀 Desplegando aplicación a Railway..." -ForegroundColor Green
railway up

Write-Host "✅ Despliegue completado!" -ForegroundColor Green
Write-Host "🌐 La aplicación estará disponible en: https://tu-app.railway.app" -ForegroundColor Cyan
Write-Host "📊 Para ver los logs: railway logs" -ForegroundColor Cyan
Write-Host "🔧 Para abrir en el navegador: railway open" -ForegroundColor Cyan
