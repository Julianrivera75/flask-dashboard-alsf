# 🚀 GeoServer en AWS Free Tier - Guía Completa

## 📋 **Requisitos AWS Free Tier:**

### **✅ Incluido Gratis (12 meses):**
- **EC2**: 750 horas/mes (t2.micro)
- **S3**: 5GB almacenamiento
- **RDS**: 750 horas/mes (db.t3.micro)
- **CloudFront**: 50GB transferencia
- **Route 53**: 1 zona hospedada

### **⚠️ Limitaciones:**
- **EC2 t2.micro**: 1 vCPU, 1GB RAM
- **RDS db.t3.micro**: 1 vCPU, 1GB RAM
- **Transferencia**: 15GB/mes

## 🏗️ **Arquitectura Recomendada:**

```
Internet → CloudFront → ALB → EC2 (GeoServer) → RDS (PostGIS)
```

## 📝 **Paso 1: Crear EC2 Instance**

### **A. Configuración EC2:**
- **AMI**: Amazon Linux 2
- **Instance Type**: t2.micro (Free Tier)
- **Storage**: 8GB EBS (Free Tier)
- **Security Group**: 
  - SSH (22)
  - HTTP (80)
  - HTTPS (443)
  - Custom (8080) - GeoServer

### **B. User Data Script:**
```bash
#!/bin/bash
yum update -y
yum install -y java-11-openjdk wget unzip nginx

# Crear usuario
useradd geoserver

# Descargar GeoServer
cd /opt
wget https://github.com/geoserver/geoserver/releases/download/2.24.0/geoserver-2.24.0-bin.zip
unzip geoserver-2.24.0-bin.zip
mv geoserver-2.24.0 geoserver
chown -R geoserver:geoserver /opt/geoserver

# Configurar servicio
cat > /etc/systemd/system/geoserver.service << EOF
[Unit]
Description=GeoServer
After=network.target

[Service]
Type=forking
User=geoserver
ExecStart=/opt/geoserver/bin/startup.sh
ExecStop=/opt/geoserver/bin/shutdown.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable geoserver
systemctl start geoserver
```

## 🗄️ **Paso 2: Configurar RDS PostGIS**

### **A. Crear RDS Instance:**
- **Engine**: PostgreSQL
- **Version**: 13.x
- **Instance**: db.t3.micro
- **Storage**: 20GB (mínimo)
- **Multi-AZ**: No (para Free Tier)

### **B. Instalar PostGIS:**
```sql
-- Conectar a RDS
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

## 🔧 **Paso 3: Configurar GeoServer**

### **A. Acceder a GeoServer:**
```
http://tu-ec2-ip:8080/geoserver
Usuario: admin
Contraseña: geoserver
```

### **B. Configurar Datastore:**
1. **Workspaces** → Crear "santafe"
2. **Stores** → Add new Store → PostGIS
3. **Configuración:**
   - **Data Source Name**: santafe_db
   - **Database**: tu_rds_endpoint
   - **Schema**: public
   - **User**: tu_usuario
   - **Password**: tu_password

## 💰 **Costos Estimados (Free Tier):**

### **✅ Gratis (12 meses):**
- **EC2 t2.micro**: $0/mes
- **RDS db.t3.micro**: $0/mes
- **S3 5GB**: $0/mes
- **CloudFront 50GB**: $0/mes

### **⚠️ Posibles costos:**
- **Transferencia extra**: $0.09/GB
- **S3 extra**: $0.023/GB
- **RDS storage extra**: $0.115/GB

## 🚀 **Paso 4: Optimización para Free Tier**

### **A. Configuración Java:**
```bash
# /opt/geoserver/bin/setenv.sh
export JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"
```

### **B. Configuración Tomcat:**
```xml
<!-- /opt/geoserver/webapps/geoserver/WEB-INF/web.xml -->
<Connector port="8080" 
           maxThreads="10" 
           minSpareThreads="2"
           maxConnections="100" />
```

### **C. Configuración PostGIS:**
```sql
-- Optimizar para recursos limitados
ALTER SYSTEM SET shared_buffers = '128MB';
ALTER SYSTEM SET effective_cache_size = '256MB';
ALTER SYSTEM SET work_mem = '4MB';
```

## 🔄 **Paso 5: Integración con tu App Flask**

### **A. Variables de Entorno:**
```bash
GEOSERVER_URL=http://tu-ec2-ip:8080/geoserver
GEOSERVER_ADMIN_USER=admin
GEOSERVER_ADMIN_PASSWORD=geoserver
```

### **B. Configuración en Railway:**
```json
{
  "environments": {
    "production": {
      "variables": {
        "GEOSERVER_URL": "http://tu-ec2-ip:8080/geoserver",
        "GEOSERVER_ADMIN_USER": "admin",
        "GEOSERVER_ADMIN_PASSWORD": "geoserver"
      }
    }
  }
}
```

## 📊 **Monitoreo de Costos:**

### **A. AWS Cost Explorer:**
- Revisar diariamente
- Configurar alertas
- Establecer presupuesto

### **B. Alertas Recomendadas:**
- **$5/mes** - Advertencia
- **$10/mes** - Crítico
- **$15/mes** - Parar servicios

## 🎯 **Ventajas vs Railway:**

| Aspecto | AWS Free Tier | Railway |
|---------|---------------|---------|
| **Costo** | $0 (12 meses) | $5 crédito |
| **Recursos** | Limitados | Generosos |
| **Control** | Completo | Limitado |
| **Complejidad** | Alta | Baja |
| **Escalabilidad** | Alta | Media |

## 🚨 **Recomendación:**

### **Para tu caso:**
1. **Empezar con Railway** - Más simple
2. **Migrar a AWS** - Si necesitas más control
3. **Híbrido** - Railway para desarrollo, AWS para producción

¿Te gustaría que te ayude a configurar AWS paso a paso? 