#!/usr/bin/env python3
"""
Script de migración a producción
Migra datos de SQLite a PostgreSQL y prepara archivos estáticos
"""

import os
import sys
import shutil
import sqlite3
import psycopg2
import json
from datetime import datetime
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'psycopg2-binary',
        'boto3',
        'gunicorn',
        'Flask-SQLAlchemy',
        'Flask-Login'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("📦 Instale con: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def backup_sqlite_database():
    """Crea un backup de la base de datos SQLite"""
    print("📦 Creando backup de SQLite...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backup_sqlite_{timestamp}.db"
    
    if os.path.exists("app.db"):
        shutil.copy2("app.db", backup_path)
        print(f"✅ Backup creado: {backup_path}")
        return backup_path
    else:
        print("⚠️ No se encontró app.db")
        return None

def migrate_users_to_postgresql(sqlite_backup, postgres_url):
    """Migra usuarios de SQLite a PostgreSQL"""
    print("👥 Migrando usuarios a PostgreSQL...")
    
    try:
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect(sqlite_backup or "app.db")
        sqlite_cursor = sqlite_conn.cursor()
        
        # Conectar a PostgreSQL
        pg_conn = psycopg2.connect(postgres_url)
        pg_cursor = pg_conn.cursor()
        
        # Crear tabla de usuarios si no existe
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP
            )
        """)
        
        # Obtener usuarios de SQLite
        sqlite_cursor.execute('SELECT * FROM users')
        users = sqlite_cursor.fetchall()
        
        migrated_count = 0
        for user_data in users:
            try:
                # Insertar en PostgreSQL
                pg_cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, role, is_active, created_at, last_login, failed_login_attempts, locked_until)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                """, user_data[1:])
                migrated_count += 1
            except Exception as e:
                print(f"⚠️ Error migrando usuario {user_data[1]}: {e}")
        
        pg_conn.commit()
        print(f"✅ {migrated_count} usuarios migrados exitosamente")
        
        sqlite_conn.close()
        pg_conn.close()
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        return False
    
    return True

def optimize_images():
    """Optimiza imágenes para producción"""
    print("🖼️ Optimizando imágenes...")
    
    images_dir = Path("static/images")
    if not images_dir.exists():
        print("⚠️ No se encontró directorio de imágenes")
        return
    
    # Verificar si jpegoptim está instalado
    if os.system("which jpegoptim > /dev/null 2>&1") != 0:
        print("⚠️ jpegoptim no está instalado. Instale con: sudo apt install jpegoptim")
        return
    
    # Verificar si optipng está instalado
    if os.system("which optipng > /dev/null 2>&1") != 0:
        print("⚠️ optipng no está instalado. Instale con: sudo apt install optipng")
        return
    
    # Optimizar imágenes
    jpg_count = 0
    png_count = 0
    
    for jpg_file in images_dir.rglob("*.jpg"):
        os.system(f"jpegoptim --strip-all '{jpg_file}'")
        jpg_count += 1
    
    for png_file in images_dir.rglob("*.png"):
        os.system(f"optipng '{png_file}'")
        png_count += 1
    
    print(f"✅ {jpg_count} imágenes JPG optimizadas")
    print(f"✅ {png_count} imágenes PNG optimizadas")

def create_production_config():
    """Crea archivo de configuración para producción"""
    print("⚙️ Creando configuración de producción...")
    
    config_template = """# Configuración de producción
import os
from datetime import timedelta

class ProductionConfig:
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambiar-en-produccion')
    DEBUG = False
    TESTING = False
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Seguridad
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = '/var/www/uploads'
    STATIC_FOLDER = '/var/www/static'
    
    # Google Sheets
    SHEET_ID = os.environ.get('SHEET_ID')
    GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH')
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/indicadores/app.log'
"""
    
    with open("config/production.py", "w") as f:
        f.write(config_template)
    
    print("✅ Configuración de producción creada: config/production.py")

def create_deployment_scripts():
    """Crea scripts de despliegue"""
    print("📜 Creando scripts de despliegue...")
    
    # Script de despliegue
    deploy_script = """#!/bin/bash
# Script de despliegue automático

echo "🚀 Iniciando despliegue..."

# Variables
APP_DIR="/var/www/indicadores"
BACKUP_DIR="/var/backups/indicadores"
LOG_FILE="/var/log/indicadores/deploy.log"

# Crear directorios si no existen
sudo mkdir -p $APP_DIR
sudo mkdir -p $BACKUP_DIR
sudo mkdir -p /var/log/indicadores

# Backup de la base de datos
echo "📦 Creando backup de la base de datos..."
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql

# Actualizar código
echo "📥 Actualizando código..."
cd $APP_DIR
git pull origin main

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Migrar base de datos
echo "🗄️ Migrando base de datos..."
flask db upgrade

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
flask collect-static --noinput

# Reiniciar servicios
echo "🔄 Reiniciando servicios..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "✅ Despliegue completado!"
echo "📊 Logs disponibles en: $LOG_FILE"
"""
    
    # Script de monitoreo
    monitor_script = """#!/bin/bash
# Script de monitoreo

echo "📊 Estado de los servicios:"

# Verificar servicios
echo "🔍 Verificando servicios..."
systemctl is-active --quiet gunicorn && echo "✅ Gunicorn: Activo" || echo "❌ Gunicorn: Inactivo"
systemctl is-active --quiet nginx && echo "✅ Nginx: Activo" || echo "❌ Nginx: Inactivo"
systemctl is-active --quiet postgresql && echo "✅ PostgreSQL: Activo" || echo "❌ PostgreSQL: Inactivo"

# Verificar espacio en disco
echo "💾 Espacio en disco:"
df -h | grep -E '^/dev/'

# Verificar logs recientes
echo "📝 Logs recientes:"
tail -n 5 /var/log/nginx/error.log 2>/dev/null || echo "No hay logs de Nginx"
tail -n 5 /var/log/gunicorn/error.log 2>/dev/null || echo "No hay logs de Gunicorn"
"""
    
    # Crear directorio scripts si no existe
    os.makedirs("scripts", exist_ok=True)
    
    # Escribir scripts
    with open("scripts/deploy.sh", "w") as f:
        f.write(deploy_script)
    
    with open("scripts/monitor.sh", "w") as f:
        f.write(monitor_script)
    
    # Hacer ejecutables
    os.chmod("scripts/deploy.sh", 0o755)
    os.chmod("scripts/monitor.sh", 0o755)
    
    print("✅ Scripts creados:")
    print("   📜 scripts/deploy.sh")
    print("   📜 scripts/monitor.sh")

def create_nginx_config():
    """Crea configuración de Nginx"""
    print("🌐 Creando configuración de Nginx...")
    
    nginx_config = """server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;
    
    # SSL Configuration (configurar después)
    # ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Static Files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health Check
    location /health {
        access_log off;
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }
}
"""
    
    os.makedirs("config/nginx", exist_ok=True)
    with open("config/nginx/indicadores.conf", "w") as f:
        f.write(nginx_config)
    
    print("✅ Configuración de Nginx creada: config/nginx/indicadores.conf")

def create_systemd_service():
    """Crea archivo de servicio systemd"""
    print("🔧 Creando servicio systemd...")
    
    service_config = """[Unit]
Description=Indicadores de Gestión Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/indicadores
Environment="PATH=/var/www/indicadores/venv/bin"
Environment="FLASK_APP=app_with_auth.py"
Environment="FLASK_ENV=production"
ExecStart=/var/www/indicadores/venv/bin/gunicorn --config gunicorn.conf.py app_with_auth:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    with open("config/indicadores.service", "w") as f:
        f.write(service_config)
    
    print("✅ Servicio systemd creado: config/indicadores.service")

def main():
    """Función principal"""
    print("🚀 Migración a Producción - Indicadores de Gestión")
    print("=" * 60)
    
    # Verificar dependencias
    if not check_requirements():
        return
    
    # Backup de SQLite
    backup_path = backup_sqlite_database()
    
    # Preguntar por configuración de PostgreSQL
    print("\n🗄️ Configuración de PostgreSQL:")
    postgres_url = input("URL de conexión PostgreSQL (ej: postgresql://user:pass@host:port/db): ").strip()
    
    if postgres_url:
        # Migrar usuarios
        if migrate_users_to_postgresql(backup_path, postgres_url):
            print("✅ Migración de usuarios completada")
        else:
            print("❌ Error en migración de usuarios")
    
    # Optimizar imágenes
    optimize_images()
    
    # Crear archivos de configuración
    create_production_config()
    create_deployment_scripts()
    create_nginx_config()
    create_systemd_service()
    
    print("\n🎉 Migración completada!")
    print("\n📋 Próximos pasos:")
    print("1. 🔧 Configurar variables de entorno en el servidor")
    print("2. 🌐 Configurar dominio y DNS")
    print("3. 🔒 Obtener certificado SSL con Let's Encrypt")
    print("4. 🚀 Ejecutar scripts de despliegue")
    print("5. 📊 Configurar monitoreo y backups")
    
    print("\n📚 Documentación disponible en: docs/PRODUCTION_DEPLOYMENT.md")

if __name__ == '__main__':
    main() 