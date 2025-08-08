#!/bin/bash

# Script para desplegar la aplicación Flask a Railway

echo "🚀 Iniciando despliegue a Railway..."

# Verificar que Railway CLI esté instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado. Instalando..."
    npm install -g @railway/cli
fi

# Verificar que estemos en el directorio correcto
if [ ! -f "wsgi.py" ]; then
    echo "❌ Error: No se encontró wsgi.py. Asegúrate de estar en el directorio correcto."
    exit 1
fi

# Verificar que los archivos necesarios existan
echo "📋 Verificando archivos necesarios..."
required_files=("Dockerfile.flask" "railway.json" "requirements.txt" "wsgi.py" "app_modular.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: No se encontró $file"
        exit 1
    fi
done

echo "✅ Todos los archivos necesarios están presentes"

# Iniciar sesión en Railway (si no está ya logueado)
echo "🔐 Verificando sesión de Railway..."
railway login

# Desplegar a Railway
echo "🚀 Desplegando aplicación a Railway..."
railway up

echo "✅ Despliegue completado!"
echo "🌐 La aplicación estará disponible en: https://tu-app.railway.app"
echo "📊 Para ver los logs: railway logs"
echo "🔧 Para abrir en el navegador: railway open"
