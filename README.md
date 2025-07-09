# 📊 Dashboard de Cifras y Gráficas

Una aplicación web en Python que muestra cifras y gráficas en tiempo real desde Google Sheets, con un diseño moderno usando los colores de la Alcaldía Mayor de Bogotá.

## 🎨 Características

- **Fondo blanco** con colores secundarios `#fab62d` (amarillo) y `#e4032e` (rojo)
- **Gráficas interactivas** usando Plotly.js
- **Actualización automática** cada hora
- **Diseño responsivo** para móviles y desktop
- **Interfaz intuitiva** y fácil de usar
- **Conexión directa** con Google Sheets

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Google Sheets API

#### Paso 1: Crear proyecto en Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Sheets API** y **Google Drive API**

#### Paso 2: Crear credenciales de servicio
1. Ve a "APIs y servicios" > "Credenciales"
2. Haz clic en "Crear credenciales" > "Cuenta de servicio"
3. Completa la información:
   - **Nombre**: `dashboard-sheets`
   - **Descripción**: `Cuenta de servicio para dashboard`
4. Haz clic en "Crear y continuar"
5. En "Otorgar acceso a esta cuenta de servicio", selecciona "Editor"
6. Haz clic en "Listo"

#### Paso 3: Descargar credenciales
1. En la lista de cuentas de servicio, haz clic en la que creaste
2. Ve a la pestaña "Claves"
3. Haz clic en "Agregar clave" > "Crear nueva clave"
4. Selecciona "JSON" y haz clic en "Crear"
5. Descarga el archivo JSON

#### Paso 4: Configurar credenciales
1. Renombra el archivo descargado a `credentials.json`
2. Colócalo en la raíz del proyecto (mismo nivel que `app.py`)

### 4. Compartir Google Sheet
1. Abre tu Google Sheet: `https://docs.google.com/spreadsheets/d/1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU/edit`
2. Haz clic en "Compartir" (esquina superior derecha)
3. Agrega el email de la cuenta de servicio (está en `credentials.json` en el campo `client_email`)
4. Dale permisos de "Editor"
5. Haz clic en "Enviar"

### 5. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📁 Estructura del proyecto

```
proyecto/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── config.env            # Configuración (ID del Google Sheet)
├── credentials.json      # Credenciales de Google (crear)
├── credentials.json.example  # Ejemplo de credenciales
├── templates/
│   └── index.html        # Página web principal
└── README.md             # Este archivo
```

## 🔧 Configuración

### Variables de entorno (`config.env`)
```env
GOOGLE_SHEET_ID=1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU
FLASK_ENV=development
FLASK_DEBUG=True
```

### Estructura recomendada del Google Sheet
- **Primera fila**: Encabezados de columnas
- **Columnas de fecha**: Nombres que contengan "fecha" o "date"
- **Columnas numéricas**: Datos que se puedan convertir a números
- **Columnas categóricas**: Texto con valores repetidos

## 📊 Tipos de gráficas generadas

1. **Gráfica de línea temporal**: Si hay columnas de fecha y numéricas
2. **Gráfica de barras**: Para mostrar valores actuales de indicadores
3. **Gráfica de pastel**: Para distribución de datos categóricos

## 🎨 Colores utilizados

- **Fondo**: `#ffffff` (Blanco)
- **Amarillo principal**: `#fab62d`
- **Rojo principal**: `#e4032e`
- **Gris oscuro**: `#333333`
- **Gris claro**: `#f5f5f5`

## 🔄 Actualización de datos

- **Automática**: Cada hora
- **Manual**: Botón "Actualizar Ahora" en la interfaz
- **Frontend**: Actualización cada 5 minutos

## 🛠️ Solución de problemas

### Error: "No se pudo conectar a Google Sheets"
- Verifica que `credentials.json` esté en la raíz del proyecto
- Asegúrate de que la cuenta de servicio tenga permisos en el Google Sheet
- Confirma que las APIs estén habilitadas en Google Cloud Console

### Error: "No hay datos disponibles"
- Verifica que el Google Sheet tenga datos
- Confirma que la primera fila contenga encabezados
- Asegúrate de que el ID del Google Sheet sea correcto

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📱 Características móviles

- Diseño responsivo
- Gráficas interactivas táctiles
- Navegación optimizada para móviles
- Tablas con scroll horizontal

## 🔒 Seguridad

- Las credenciales se mantienen locales
- No se almacenan datos sensibles
- Conexión segura con Google APIs
- Validación de datos de entrada

## 📈 Personalización

### Cambiar colores
Edita las variables CSS en `templates/index.html`:
```css
:root {
    --primary-yellow: #fab62d;
    --primary-red: #e4032e;
    --white: #ffffff;
    /* ... */
}
```

### Cambiar frecuencia de actualización
Edita en `app.py`:
```python
scheduler.add_job(func=fetch_data_from_sheets, trigger="interval", hours=1)  # Cambia "hours=1"
```

### Agregar nuevas gráficas
Modifica la función `create_charts()` en `app.py`

## 📞 Soporte

Si tienes problemas:
1. Verifica que todas las dependencias estén instaladas
2. Confirma la configuración de Google Cloud
3. Revisa los permisos del Google Sheet
4. Consulta los logs de la aplicación

## 🚀 Despliegue

### Local
```bash
python app.py
```

### Producción (recomendado)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Desarrollado con ❤️ para la Alcaldía Mayor de Bogotá** 