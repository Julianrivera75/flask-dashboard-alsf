# Indicadores de Gestión Localidad de Santa Fe

Sistema de monitoreo y seguimiento de la gestión local del barrio San Bernardo.

## 📋 Descripción

Este proyecto es una aplicación web desarrollada en Python con Flask que permite visualizar y analizar indicadores de gestión de la Alcaldía Local de Santa Fe, específicamente enfocada en el barrio San Bernardo.

## 🚀 Características

- **Dashboard Interactivo**: Visualización de indicadores clave
- **Gráficos Dinámicos**: Gráficos de participación y estadísticas
- **Integración con Google Sheets**: Datos en tiempo real
- **Responsive Design**: Compatible con dispositivos móviles
- **Menú Lateral**: Navegación intuitiva

## 🛠️ Tecnologías

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Plotly.js
- **Base de Datos**: Google Sheets API
- **Autenticación**: OAuth2 con Google

## 📁 Estructura del Proyecto

```
Carpeta/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración general
├── data_manager.py        # Manejo de datos
├── google_sheets_connector.py  # Conexión Google Sheets
├── chart_generator.py     # Generación de gráficos
├── requirements.txt       # Dependencias
├── static/                # Archivos estáticos
│   ├── css/              # Estilos CSS
│   ├── js/               # JavaScript
│   └── images/           # Imágenes
├── templates/             # Plantillas HTML
├── utils/                 # Utilidades
├── services/              # Servicios
├── models/                # Modelos de datos
├── config/                # Configuraciones
├── tests/                 # Tests
└── docs/                  # Documentación
```

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Carpeta
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Google Sheets**
   - Crear proyecto en Google Cloud Console
   - Habilitar Google Sheets API
   - Crear credenciales de servicio
   - Descargar `credentials.json`

5. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

6. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

## 📊 Uso

1. Abrir navegador en `http://localhost:5000`
2. El dashboard se cargará automáticamente
3. Usar el menú lateral para navegar
4. Los datos se actualizan automáticamente desde Google Sheets

## 🔧 Configuración

### Variables de Entorno

```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SHEET_ID=your-sheet-id
FLASK_ENV=development
FLASK_DEBUG=True
```

### Google Sheets

El proyecto espera una hoja de cálculo con las siguientes columnas:
- Entidad
- Actividad
- Fecha final de ejecución
- Población impactada

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=.

# Ejecutar tests específicos
pytest tests/test_data_manager.py
```

## 📝 Desarrollo

### Estructura Modular

El proyecto está organizado en módulos separados:

- **CSS**: `static/css/main.css` y `static/css/dashboard.css`
- **JavaScript**: `static/js/main.js` y `static/js/charts.js`
- **Python**: Servicios, utilidades y modelos separados
- **Configuración**: Diferentes configuraciones por ambiente

### Agregar Nuevas Funcionalidades

1. Crear archivo en el módulo correspondiente
2. Agregar tests
3. Actualizar documentación
4. Seguir las convenciones de código

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Equipo de Desarrollo ALSF** - *Desarrollo inicial*

## 🙏 Agradecimientos

- Google Sheets API
- Plotly.js para visualizaciones
- Comunidad de Flask 