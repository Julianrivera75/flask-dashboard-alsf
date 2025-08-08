# Despliegue en Railway

Este documento explica cómo desplegar la aplicación Flask en Railway.

## 📋 Prerrequisitos

1. **Cuenta de Railway**: Crear una cuenta en [railway.app](https://railway.app)
2. **Railway CLI**: Instalar el CLI de Railway
3. **Git**: Tener Git instalado y configurado

## 🚀 Despliegue Automático

### Opción 1: Usando el script de PowerShell (Windows)

```powershell
# Ejecutar el script de despliegue
.\deploy_railway.ps1
```

### Opción 2: Despliegue Manual

1. **Instalar Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Iniciar sesión**:
   ```bash
   railway login
   ```

3. **Inicializar proyecto** (si es la primera vez):
   ```bash
   railway init
   ```

4. **Desplegar**:
   ```bash
   railway up
   ```

## 📁 Archivos de Configuración

### Dockerfile.flask
- Configuración de Docker para la aplicación Flask
- Usa Python 3.11-slim como base
- Instala todas las dependencias necesarias
- Expone el puerto 8000

### railway.json
- Configuración específica para Railway
- Usa Dockerfile.flask como builder
- Configura health checks y variables de entorno

### .dockerignore
- Excluye archivos innecesarios del build
- Optimiza el tamaño de la imagen

## 🔧 Variables de Entorno

Configurar las siguientes variables en Railway:

### Variables Obligatorias
- `FLASK_ENV`: production
- `FLASK_APP`: wsgi.py
- `PORT`: 8000

### Variables de Google Sheets (Opcionales)
- `GOOGLE_SHEETS_CREDENTIALS_FILE`: Ruta al archivo de credenciales
- `SPREADSHEET_ID`: ID de la hoja de cálculo principal
- `GOOGLE_CREDENTIALS_JSON`: Credenciales JSON de Google (como variable de entorno)

### Variables de Seguridad
- `SECRET_KEY`: Clave secreta para Flask

## 📊 Monitoreo

### Ver Logs
```bash
railway logs
```

### Ver Estado
```bash
railway status
```

### Abrir en Navegador
```bash
railway open
```

## 🔄 Actualizaciones

Para actualizar la aplicación:

1. **Hacer cambios en el código**
2. **Commit y push a Git**:
   ```bash
   git add .
   git commit -m "Actualización"
   git push
   ```
3. **Railway detectará automáticamente los cambios y redeployará**

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
- Verificar que requirements.txt esté presente
- Revisar que todas las dependencias estén listadas

### Error: "Port already in use"
- Railway asignará automáticamente un puerto
- Verificar que el Dockerfile use `$PORT` en lugar de un puerto fijo

### Error: "Health check failed"
- Verificar que la aplicación responda en la ruta `/`
- Revisar los logs para más detalles

## 📞 Soporte

Si tienes problemas con el despliegue:

1. Revisar los logs: `railway logs`
2. Verificar el estado: `railway status`
3. Revisar la configuración de Railway en el dashboard web

## 🔗 Enlaces Útiles

- [Railway Documentation](https://docs.railway.app/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
