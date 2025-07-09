# 🚀 Configuración Rápida - Google Sheets API

## 📋 Pasos para conectar con tu Google Sheet

### 1. Crear proyecto en Google Cloud Console
1. Ve a: https://console.cloud.google.com/
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs:
   - **Google Sheets API**
   - **Google Drive API**

### 2. Crear cuenta de servicio
1. Ve a "APIs y servicios" > "Credenciales"
2. Haz clic en "Crear credenciales" > "Cuenta de servicio"
3. Nombre: `dashboard-sheets`
4. Descripción: `Cuenta de servicio para dashboard`
5. Haz clic en "Crear y continuar"
6. En permisos, selecciona "Editor"
7. Haz clic en "Listo"

### 3. Descargar credenciales
1. En la lista de cuentas de servicio, haz clic en la que creaste
2. Ve a la pestaña "Claves"
3. Haz clic en "Agregar clave" > "Crear nueva clave"
4. Selecciona "JSON"
5. Descarga el archivo

### 4. Configurar el proyecto
1. Renombra el archivo descargado a `credentials.json`
2. Colócalo en la raíz del proyecto (mismo nivel que `app.py`)

### 5. Compartir Google Sheet
1. Abre tu Google Sheet: https://docs.google.com/spreadsheets/d/1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU/edit
2. Haz clic en "Compartir" (esquina superior derecha)
3. Agrega el email de la cuenta de servicio (está en `credentials.json` en `client_email`)
4. Dale permisos de "Editor"
5. Haz clic en "Enviar"

### 6. Ejecutar aplicación completa
```bash
python app.py
```

## 🎯 Estructura recomendada del Google Sheet

| fecha       | ventas | gastos | beneficios | categoria |
|-------------|--------|--------|------------|-----------|
| 2024-01-01  | 1000   | 500    | 500        | A         |
| 2024-01-02  | 1200   | 600    | 600        | B         |
| 2024-01-03  | 800    | 400    | 400        | A         |

## 🔧 Solución de problemas

### Error: "No se pudo conectar a Google Sheets"
- ✅ Verifica que `credentials.json` esté en la raíz
- ✅ Confirma que la cuenta de servicio tenga permisos
- ✅ Asegúrate de que las APIs estén habilitadas

### Error: "No hay datos disponibles"
- ✅ Verifica que el Google Sheet tenga datos
- ✅ Confirma que la primera fila contenga encabezados
- ✅ Asegúrate de que el ID del Google Sheet sea correcto

## 📱 Versión de demostración

Si quieres probar sin configurar Google Sheets:
```bash
python app_demo.py
```

Esto te mostrará la interfaz con datos de ejemplo.

## 🎨 Colores utilizados

- **Fondo**: `#ffffff` (Blanco)
- **Amarillo**: `#fab62d`
- **Rojo**: `#e4032e`

---

**¡Listo! Tu dashboard estará disponible en http://localhost:5000** 