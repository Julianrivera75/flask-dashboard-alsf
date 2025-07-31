# 🚀 Guía de Despliegue a Producción

## 📋 Resumen de Componentes a Alojar

### 🗄️ **Base de Datos**
- **Usuarios y autenticación** (SQLite → PostgreSQL/MySQL)
- **Datos de Google Sheets** (caché local)
- **Logs de actividad**

### 📁 **Archivos Estáticos**
- **Imágenes**: Fotos de puntos críticos
- **Documentos**: PDFs, Excel, etc.
- **Archivos KML**: Mapas y coordenadas
- **CSS/JS**: Archivos de frontend

### 🖥️ **Aplicación Web**
- **Flask App**: Código Python
- **Servidor Web**: Gunicorn + Nginx
- **SSL/HTTPS**: Certificados de seguridad

---

## 🏗️ **Opciones de Alojamiento**

### 1. 🌐 **Servicios Cloud (Recomendado)**

#### **A. Heroku (Fácil)**
```bash
# Pros: Fácil despliegue, automático SSL
# Contras: Limitado en almacenamiento, costos variables

# Configuración
DATABASE_URL=postgresql://user:pass@host:port/db
STATIC_FILES=CDN o AWS S3
```

#### **B. AWS (Profesional)**
```bash
# Pros: Escalable, completo, confiable
# Contras: Complejo, requiere conocimientos

# Servicios recomendados:
- EC2: Servidor web
- RDS: Base de datos PostgreSQL
- S3: Almacenamiento de archivos
- CloudFront: CDN para archivos estáticos
- Route 53: DNS
- Certificate Manager: SSL gratuito
```

#### **C. Google Cloud Platform**
```bash
# Pros: Integración con Google Sheets, confiable
# Contras: Costos, complejidad

# Servicios:
- App Engine: Aplicación web
- Cloud SQL: Base de datos
- Cloud Storage: Archivos
- Cloud CDN: Distribución de contenido
```

#### **D. DigitalOcean (Económico)**
```bash
# Pros: Económico, fácil de usar
# Contras: Menos servicios integrados

# Configuración:
- Droplet: Servidor VPS
- Managed Database: PostgreSQL
- Spaces: Almacenamiento de archivos
```

### 2. 🏢 **Hosting Tradicional**

#### **A. VPS (Virtual Private Server)**
```bash
# Proveedores recomendados:
- DigitalOcean ($5-20/mes)
- Linode ($5-20/mes)
- Vultr ($2.50-20/mes)
- AWS Lightsail ($3.50-20/mes)
```

#### **B. Hosting Compartido**
```bash
# Solo para aplicaciones pequeñas
# Limitaciones: Sin acceso SSH, sin control total
```

---

## 📊 **Estructura de Datos en Producción**

### 🗄️ **Base de Datos PostgreSQL**

```sql
-- Tabla de usuarios
CREATE TABLE users (
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
);

-- Tabla de datos de Google Sheets (caché)
CREATE TABLE sheet_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sheet_id VARCHAR(100) NOT NULL
);

-- Tabla de logs de actividad
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📁 **Estructura de Archivos**

```
/production/
├── app/                    # Código de la aplicación
│   ├── static/
│   │   ├── images/        # Imágenes optimizadas
│   │   ├── docs/          # Documentos
│   │   ├── kml/           # Archivos KML
│   │   └── uploads/       # Archivos subidos por usuarios
│   └── templates/
├── data/                   # Datos persistentes
│   ├── database/          # Base de datos
│   ├── logs/              # Logs de aplicación
│   └── cache/             # Caché de Google Sheets
└── config/                # Configuraciones
    ├── nginx/
    ├── gunicorn/
    └── environment/
```

---

## 🚀 **Plan de Despliegue Paso a Paso**

### **Fase 1: Preparación**

#### 1.1 **Optimizar Código**
```python
# config/production.py
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    WTF_CSRF_ENABLED = True
    
    # Configuración de archivos estáticos
    STATIC_FOLDER = '/var/www/static'
    UPLOAD_FOLDER = '/var/www/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
```

#### 1.2 **Preparar Archivos**
```bash
# Optimizar imágenes
find static/images -name "*.jpg" -exec jpegoptim --strip-all {} \;
find static/images -name "*.png" -exec optipng {} \;

# Comprimir archivos estáticos
gzip -9 static/css/*.css
gzip -9 static/js/*.js
```

#### 1.3 **Configurar Variables de Entorno**
```env
# .env.production
SECRET_KEY=tu-clave-super-secreta-y-muy-larga
DATABASE_URL=postgresql://user:pass@host:port/db
SHEET_ID=tu-google-sheet-id
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### **Fase 2: Base de Datos**

#### 2.1 **Migrar de SQLite a PostgreSQL**
```python
# scripts/migrate_db.py
import sqlite3
import psycopg2
from models.user import User, db

def migrate_users():
    # Conectar a SQLite
    sqlite_conn = sqlite3.connect('app.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Obtener usuarios
    sqlite_cursor.execute('SELECT * FROM users')
    users = sqlite_cursor.fetchall()
    
    # Migrar a PostgreSQL
    for user_data in users:
        user = User(
            email=user_data[1],
            password_hash=user_data[2],
            first_name=user_data[3],
            last_name=user_data[4],
            role=user_data[5]
        )
        db.session.add(user)
    
    db.session.commit()
```

#### 2.2 **Configurar Backup Automático**
```bash
#!/bin/bash
# scripts/backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
gzip backup_$DATE.sql
aws s3 cp backup_$DATE.sql.gz s3://tu-bucket/backups/
```

### **Fase 3: Servidor Web**

#### 3.1 **Configurar Nginx**
```nginx
# /etc/nginx/sites-available/indicadores
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
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
}
```

#### 3.2 **Configurar Gunicorn**
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

### **Fase 4: Almacenamiento de Archivos**

#### 4.1 **AWS S3 (Recomendado)**
```python
# services/storage_service.py
import boto3
from botocore.exceptions import ClientError

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'tu-bucket-indicadores'
    
    def upload_file(self, file_path, s3_key):
        try:
            self.s3.upload_file(file_path, self.bucket, s3_key)
            return f"https://{self.bucket}.s3.amazonaws.com/{s3_key}"
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return None
    
    def get_file_url(self, s3_key, expires_in=3600):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print(f"Error generating URL: {e}")
            return None
```

#### 4.2 **Configurar CDN**
```python
# config/production.py
class ProductionConfig(Config):
    # CDN Configuration
    CDN_DOMAIN = 'cdn.tu-dominio.com'
    STATIC_URL_PREFIX = 'https://cdn.tu-dominio.com'
    
    # S3 Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_S3_REGION = os.environ.get('AWS_S3_REGION', 'us-east-1')
```

---

## 💰 **Costos Estimados (Mensual)**

### **Opción Económica (DigitalOcean)**
- VPS: $10-20/mes
- Base de datos: $15/mes
- Almacenamiento: $5/mes
- **Total: ~$30-40/mes**

### **Opción Profesional (AWS)**
- EC2: $20-50/mes
- RDS: $30-100/mes
- S3: $5-20/mes
- CloudFront: $5-15/mes
- **Total: ~$60-185/mes**

### **Opción Fácil (Heroku)**
- Dyno: $25-50/mes
- Postgres: $50-200/mes
- **Total: ~$75-250/mes**

---

## 🔧 **Scripts de Despliegue**

### **Deploy Script**
```bash
#!/bin/bash
# scripts/deploy.sh

echo "🚀 Iniciando despliegue..."

# 1. Backup de la base de datos
echo "📦 Creando backup..."
./scripts/backup_db.sh

# 2. Actualizar código
echo "📥 Actualizando código..."
git pull origin main

# 3. Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# 4. Migrar base de datos
echo "🗄️ Migrando base de datos..."
flask db upgrade

# 5. Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
flask collect-static

# 6. Reiniciar servicios
echo "🔄 Reiniciando servicios..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "✅ Despliegue completado!"
```

### **Monitoring Script**
```bash
#!/bin/bash
# scripts/monitor.sh

# Verificar servicios
systemctl is-active --quiet gunicorn || echo "❌ Gunicorn no está ejecutándose"
systemctl is-active --quiet nginx || echo "❌ Nginx no está ejecutándose"
systemctl is-active --quiet postgresql || echo "❌ PostgreSQL no está ejecutándose"

# Verificar espacio en disco
df -h | grep -E '^/dev/'

# Verificar logs
tail -n 20 /var/log/nginx/error.log
tail -n 20 /var/log/gunicorn/error.log
```

---

## 🛡️ **Seguridad en Producción**

### **Firewall**
```bash
# Configurar UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### **SSL/TLS**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com
```

### **Backup Automático**
```bash
# Crontab para backups diarios
0 2 * * * /path/to/scripts/backup_db.sh
0 3 * * * /path/to/scripts/backup_files.sh
```

---

## 📊 **Monitoreo y Logs**

### **Logs de Aplicación**
```python
# config/production.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler(
            'logs/indicadores.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Indicadores startup')
```

### **Health Check**
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': check_database_connection(),
        'google_sheets': check_google_sheets_connection()
    })
```

---

## 🚨 **Checklist de Producción**

### **Antes del Despliegue**
- [ ] Cambiar SECRET_KEY
- [ ] Configurar HTTPS
- [ ] Configurar firewall
- [ ] Configurar backups
- [ ] Optimizar imágenes
- [ ] Configurar monitoreo
- [ ] Probar en staging

### **Después del Despliegue**
- [ ] Verificar SSL
- [ ] Probar todas las funcionalidades
- [ ] Configurar alertas
- [ ] Documentar credenciales
- [ ] Configurar DNS
- [ ] Probar backups

---

**💡 Recomendación**: Para empezar, usa **DigitalOcean** con un VPS de $10/mes. Es económico, fácil de configurar y puedes escalar después. 