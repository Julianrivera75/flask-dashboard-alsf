# 🏛️ Alcaldía Mayor de Bogotá - Dashboard (Versión POO)

## 📋 Descripción

Dashboard web para la Alcaldía Mayor de Bogotá que muestra datos de actividades y compromisos obtenidos desde Google Sheets. Esta versión utiliza **Programación Orientada a Objetos (POO)** para una mejor organización y mantenibilidad del código.

## 🏗️ Arquitectura POO

### Estructura de Clases

```
📁 Proyecto/
├── 🏗️ app_oop.py              # Clase principal de la aplicación
├── 📊 data_manager.py         # Gestión y procesamiento de datos
├── 🔗 google_sheets_connector.py  # Conexión a Google Sheets
├── 📈 chart_generator.py      # Generación de gráficos
├── ⚙️ config.py              # Configuración centralizada
├── 🌐 templates/
│   └── index.html            # Interfaz de usuario
└── 📄 requirements.txt       # Dependencias
```

### Clases Principales

#### 1. **BogotaApp** (`app_oop.py`)
- **Responsabilidad**: Clase principal que coordina toda la aplicación
- **Funciones**:
  - Configuración de rutas Flask
  - Gestión del programador de tareas
  - Inicialización de componentes

#### 2. **DataManager** (`data_manager.py`)
- **Responsabilidad**: Gestión y procesamiento de datos
- **Funciones**:
  - Normalización de fechas
  - Cálculo de indicadores
  - Gestión del estado de datos
  - Reseteo de contadores

#### 3. **GoogleSheetsConnector** (`google_sheets_connector.py`)
- **Responsabilidad**: Conexión y obtención de datos de Google Sheets
- **Funciones**:
  - Autenticación con Google Sheets
  - Obtención de datos
  - Manejo de errores de conexión

#### 4. **ChartGenerator** (`chart_generator.py`)
- **Responsabilidad**: Generación de visualizaciones
- **Funciones**:
  - Gráfico de pie (participación por entidad)
  - Gráfico diario (actividades por día)
  - Gráfico mensual (por entidad)
  - Resúmenes de actividades

#### 5. **Config** (`config.py`)
- **Responsabilidad**: Configuración centralizada
- **Contenido**:
  - IDs de Google Sheets
  - Colores de gráficos
  - Configuraciones de la aplicación
  - Constantes importantes

## 🚀 Ventajas de la Arquitectura POO

### ✅ **Separación de Responsabilidades**
- Cada clase tiene una función específica y bien definida
- Fácil identificación de dónde hacer cambios

### ✅ **Mantenibilidad**
- Código más organizado y fácil de entender
- Modificaciones localizadas en clases específicas

### ✅ **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Reutilización de componentes

### ✅ **Testabilidad**
- Cada clase se puede probar independientemente
- Mejor cobertura de pruebas

### ✅ **Reutilización**
- Las clases se pueden usar en otros proyectos
- Configuración centralizada y reutilizable

## 🛠️ Instalación y Uso

### 1. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 2. **Configurar Google Sheets**
- Crear archivo `credentials.json` con credenciales de servicio
- Configurar `config.env` con el ID de la hoja

### 3. **Ejecutar aplicación POO**
```bash
python app_oop.py
```

## 🔄 Migración desde Versión Procedural

### Cambios Principales:

1. **Organización**: Código dividido en clases especializadas
2. **Configuración**: Centralizada en `Config`
3. **Mantenimiento**: Más fácil de modificar y extender
4. **Legibilidad**: Código más claro y estructurado

### Compatibilidad:
- ✅ Misma funcionalidad que la versión original
- ✅ Mismas APIs y endpoints
- ✅ Misma interfaz de usuario
- ✅ Mismos datos y gráficos

## 📊 Funcionalidades

### Dashboard Principal
- 📈 Gráfico de pie con participación por entidad
- 📅 Gráfico diario de actividades
- 🏆 Top 3 de entidades con más participación
- 📊 Indicadores en tiempo real

### Funcionalidades por Entidad
- 📋 Resumen de actividades
- 📅 Gráfico mensual de actividades
- ⚠️ Actividades sin fechas
- 📊 Estadísticas específicas

### Gestión de Datos
- 🔄 Actualización automática cada hora
- 🔄 Actualización manual con botón
- 📅 Normalización automática de fechas
- 🔢 Cálculo automático de indicadores

## 🎨 Personalización

### Colores y Estilos
```python
# En config.py
CHART_COLORS = {
    'marzo': '#FF6B6B',
    'abril': '#4ECDC4',
    'alcaldia': '#FF6B6B',  # Rojo para Alcaldía
    'default': '#4ECDC4'    # Verde por defecto
}
```

### Configuración de Columnas
```python
# En config.py
IMPORTANT_COLUMNS = {
    'entidad': 'Entidad',
    'poblacion': 'Población impactada',
    'fecha_ejecucion': 'Fecha final de ejecución',
    'resumen': 'Resumen de actividades'
}
```

## 🔧 Desarrollo

### Agregar Nueva Funcionalidad

1. **Identificar la clase responsable**
2. **Agregar método en la clase correspondiente**
3. **Actualizar configuración si es necesario**
4. **Agregar ruta en BogotaApp si es necesario**

### Ejemplo: Agregar Nuevo Gráfico
```python
# En ChartGenerator
def create_new_chart(self):
    # Lógica del nuevo gráfico
    pass

# En BogotaApp
@self.app.route('/api/new-chart')
def get_new_chart():
    return jsonify(self.chart_generator.create_new_chart())
```

## 📝 Notas Técnicas

- **Framework**: Flask
- **Gráficos**: Plotly
- **Datos**: Google Sheets API
- **Programación**: Orientada a Objetos
- **Configuración**: Centralizada
- **Scheduler**: APScheduler

## 🎯 Beneficios para el Equipo

1. **Desarrollo**: Código más fácil de entender y modificar
2. **Mantenimiento**: Cambios localizados y controlados
3. **Escalabilidad**: Fácil agregar nuevas características
4. **Colaboración**: Mejor división de trabajo entre desarrolladores
5. **Calidad**: Código más robusto y testeable 