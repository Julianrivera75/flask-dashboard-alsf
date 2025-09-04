# Configuración de Railway para ALSF

## Pasos para configurar la aplicación en Railway

### 1. Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub

### 2. Crear nuevo proyecto
1. Haz clic en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Conecta el repositorio de ALSF

### 3. Agregar bases de datos PostgreSQL
**Base de datos para 1000 acciones (ya existe):**
- Esta base de datos ya está configurada y contiene los datos de "1000 acciones en 1 día"
- Railway ya creó la variable `DATABASE_URL` para esta base de datos

**Base de datos para reportes de seguridad (nueva):**
1. En el dashboard del proyecto, haz clic en "New"
2. Selecciona "Database" → "PostgreSQL"
3. Nombra la base de datos como "reportes-seguridad"
4. Railway creará automáticamente la variable `REPORTES_DATABASE_URL`

### 4. Configurar variables de entorno
En el dashboard del proyecto, ve a "Variables" y agrega:

```
SECRET_KEY=tu_clave_secreta_super_segura_para_railway_2024
DATABASE_URL=postgresql://... (ya configurada por Railway para 1000 acciones)
REPORTES_DATABASE_URL=postgresql://... (configurada por Railway para reportes)
GOOGLE_SHEET_ID=1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU
SAN_BERNARDO_SHEET_ID=1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU
EL_CONSUELO_SHEET_ID=1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM
```

**Nota importante:**
- `DATABASE_URL`: Para "1000 acciones en 1 día" (ya existe)
- `REPORTES_DATABASE_URL`: Para "Santa Fe Camina Segura: Reportes de Seguridad y Convivencia" (nueva)

### 5. Configurar Google Sheets (Opcional)
Si necesitas acceso a Google Sheets, agrega:

```
GOOGLE_CREDENTIALS_JSON=tu_json_de_credenciales_aqui
GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON=credenciales_san_bernardo
GOOGLE_CREDENTIALS_CONSUELO_JSON=credenciales_consuelo
```

### 6. Desplegar
1. Railway detectará automáticamente el `Dockerfile.flask`
2. El despliegue comenzará automáticamente
3. La base de datos se inicializará automáticamente

### 7. Verificar despliegue
1. Ve a la pestaña "Deployments"
2. Espera a que el despliegue se complete
3. Haz clic en el dominio generado para acceder a la aplicación

## Estructura de las bases de datos

### Base de datos de 1000 acciones (DATABASE_URL)
Esta base de datos ya existe y contiene:
- Datos de actividades de "1000 acciones en 1 día"
- Información de Google Sheets
- Datos históricos existentes

### Base de datos de reportes (REPORTES_DATABASE_URL)
La aplicación creará automáticamente las siguientes tablas:

- `users` - Usuarios del sistema de reportes
- `reportes` - Reportes de seguridad y convivencia
- `responsables` - Responsables de actividades
- `tipos_actividad` - Tipos de actividades de seguridad
- `sectores` - Sectores catastrales
- `entidades` - Entidades participantes
- `resultados_reporte` - Resultados específicos de reportes
- `archivos_reporte` - Archivos adjuntos
- `page_views` - Analytics de páginas

## Usuarios por defecto

### Sistema de 1000 acciones
- Usuario existente (ya configurado)

### Sistema de reportes de seguridad
Se crea automáticamente un usuario administrador:
- **Usuario**: admin_reportes
- **Contraseña**: admin123
- **Email**: admin.reportes@alsf.gov.co

⚠️ **IMPORTANTE**: Cambia la contraseña del administrador después del primer login.

## Monitoreo

Railway proporciona:
- Logs en tiempo real
- Métricas de rendimiento
- Monitoreo de salud de la aplicación
- Backup automático de la base de datos

## Troubleshooting

### Error de conexión a base de datos
- Verifica que `DATABASE_URL` esté configurada
- Asegúrate de que el servicio PostgreSQL esté ejecutándose

### Error de inicialización
- Revisa los logs en Railway
- Verifica que todas las variables de entorno estén configuradas

### Error de Google Sheets
- Verifica las credenciales JSON
- Asegúrate de que los Sheet IDs sean correctos

## Comandos útiles

### Ver logs
```bash
railway logs
```

### Conectar a la base de datos
```bash
railway connect
```

### Ver variables de entorno
```bash
railway variables
```

## Costos

Railway ofrece:
- Plan gratuito con límites generosos
- $5/mes por base de datos PostgreSQL
- Escalado automático según uso

Para más información, visita la [documentación de Railway](https://docs.railway.app).
