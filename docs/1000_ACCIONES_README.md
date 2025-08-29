# Sistema "1000 Acciones en 1 Día" - Alcaldía Local Santa Fe

## Descripción General

El Sistema "1000 Acciones en 1 Día" es una plataforma web desarrollada para la Alcaldía Local Santa Fe que permite el registro, seguimiento y visualización de actividades realizadas en el marco del programa de gobierno local. El sistema está diseñado para funcionar en Railway y proporciona una interfaz intuitiva para el registro de actividades con geolocalización y gestión de archivos multimedia.

## Características Principales

### 🎯 Funcionalidades del Formulario
- **Registro de Actividades**: Formulario completo con validaciones
- **Geolocalización**: Selección de ubicación mediante mapa interactivo
- **Gestión de Archivos**: Carga y almacenamiento de fotografías
- **Validaciones**: Verificación de campos obligatorios y formatos
- **Interfaz Responsiva**: Diseño adaptable a diferentes dispositivos

### 📊 Gestión de Datos
- **Base de Datos**: PostgreSQL optimizado para Railway
- **API REST**: Endpoints para consulta y gestión de datos
- **Exportación**: Funcionalidad para descargar datos en CSV
- **Filtros Avanzados**: Búsqueda por área, tipo y fecha

### 🗺️ Visualización Geográfica
- **Mapa Interactivo**: Visualización de todas las actividades
- **Marcadores Codificados**: Colores según área responsable
- **Filtros en Tiempo Real**: Aplicación de filtros sin recargar
- **Información Detallada**: Popups con detalles de cada actividad

## Estructura del Sistema

### Modelos de Base de Datos

#### Tabla: `actividades_1000`
| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Sí |
| `nombre_responsable` | String(200) | Nombre del responsable | Sí |
| `tipo_actividad` | String(200) | Tipo de actividad realizada | Sí |
| `area_responsable` | String(100) | Área responsable | Sí |
| `area_otro` | String(200) | Especificación de otra área | No |
| `personas_impactadas` | Integer | Número de personas impactadas | Sí |
| `descripcion_detallada` | Text | Descripción de la actividad | Sí |
| `observaciones_adicionales` | Text | Observaciones adicionales | No |
| `latitud` | Float | Coordenada de latitud | Sí |
| `longitud` | Float | Coordenada de longitud | Sí |
| `fecha_creacion` | DateTime | Fecha de registro | Sí |
| `estado` | String(20) | Estado de la actividad | Sí |

#### Tabla: `fotos_actividades_1000`
| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Sí |
| `actividad_id` | Integer | Referencia a la actividad | Sí |
| `nombre_original` | String(255) | Nombre original del archivo | Sí |
| `nombre_archivo` | String(255) | Nombre del archivo en el servidor | Sí |
| `ruta_archivo` | String(500) | Ruta completa del archivo | Sí |
| `tipo_mime` | String(100) | Tipo MIME del archivo | No |
| `tamano_bytes` | BigInteger | Tamaño del archivo | No |
| `fecha_subida` | DateTime | Fecha de subida | Sí |

### Tipos de Actividades Disponibles

1. **Diálogo diferencial LGBTI**
2. **Fiesta Mayor**
3. **Feria de Emprendedoras y Productoras Locales**
4. **Recuperación entornos tramos universitarios - sector las aguas-**
5. **DANZA** (múltiples opciones)
6. **Jornada de embellecimiento**
7. **Jornada de Protección y Bienestar Animal - PYBA**
8. **MES MAYOR**
9. **INAUGURACIÓN CENTRO DE EXPERIENCIA TIC**
10. **Actividad**
11. **Encuentro**
12. **Fugate al centro**

### Áreas Responsables

- **Ambiente**
- **Seguridad**
- **Deportes**
- **Participación**
- **Innovación**
- **Planeación**
- **Otro** (con campo de especificación)

## Instalación y Configuración

### Requisitos Previos

- Python 3.8+
- PostgreSQL
- Railway CLI (para despliegue)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
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

4. **Configurar variables de entorno**
```bash
# Crear archivo .env
DATABASE_URL=postgresql://usuario:password@host:puerto/nombre_db
SECRET_KEY=tu_clave_secreta
FLASK_ENV=development
```

5. **Inicializar base de datos**
```bash
python scripts/init_acciones_1000_db.py
```

6. **Ejecutar la aplicación**
```bash
python app_modular.py
```

### Configuración para Railway

1. **Crear proyecto en Railway**
```bash
railway login
railway init
```

2. **Configurar variables de entorno en Railway**
```bash
railway variables set DATABASE_URL=postgresql://...
railway variables set SECRET_KEY=...
railway variables set FLASK_ENV=production
```

3. **Desplegar aplicación**
```bash
railway up
```

## Uso del Sistema

### Registro de Nueva Actividad

1. **Acceder al formulario**: Navegar a `/acciones-1000/`
2. **Completar información básica**:
   - Nombre del responsable
   - Tipo de actividad
   - Área responsable
   - Número de personas impactadas
3. **Describir la actividad**: Campo obligatorio para detalles
4. **Seleccionar ubicación**: Hacer clic en el mapa
5. **Adjuntar fotografías**: Cargar archivos de imagen
6. **Enviar formulario**: Validación automática antes del envío

### Visualización de Actividades

#### Lista de Actividades (`/acciones-1000/listar`)
- Tabla con todas las actividades registradas
- Filtros por área, tipo y fecha
- Estadísticas en tiempo real
- Exportación de datos a CSV

#### Mapa de Actividades (`/acciones-1000/mapa`)
- Visualización geográfica de todas las actividades
- Marcadores codificados por color según área
- Filtros aplicables en tiempo real
- Información detallada en popups

### API REST

#### Endpoint: `GET /acciones-1000/api/actividades`
```json
{
  "success": true,
  "actividades": [
    {
      "id": 1,
      "nombre_responsable": "Juan Pérez",
      "tipo_actividad": "DANZA",
      "area_responsable": "Deportes",
      "personas_impactadas": 50,
      "latitud": 4.7110,
      "longitud": -74.0721,
      "fecha_creacion": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

## Estructura de Archivos

```
├── models/
│   └── acciones_1000.py          # Modelos de base de datos
├── forms/
│   └── acciones_1000_form.py     # Formularios de validación
├── routes/
│   └── acciones_1000_routes.py   # Rutas y controladores
├── templates/acciones_1000/
│   ├── index.html                # Formulario principal
│   ├── listar.html               # Lista de actividades
│   └── mapa.html                 # Mapa de actividades
├── static/
│   ├── css/
│   │   └── acciones_1000.css     # Estilos específicos
│   └── js/
│       ├── acciones_1000.js      # JavaScript del formulario
│       ├── acciones_1000_listar.js # JavaScript de la lista
│       └── acciones_1000_mapa.js # JavaScript del mapa
├── scripts/
│   └── init_acciones_1000_db.py  # Script de inicialización
└── docs/
    └── 1000_ACCIONES_README.md   # Esta documentación
```

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework web principal
- **SQLAlchemy**: ORM para base de datos
- **PostgreSQL**: Base de datos principal
- **Werkzeug**: Manejo de archivos

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos y diseño responsivo
- **JavaScript ES6+**: Funcionalidad interactiva
- **Leaflet**: Biblioteca de mapas
- **DataTables**: Tablas interactivas
- **SweetAlert2**: Alertas y notificaciones

### Despliegue
- **Railway**: Plataforma de hosting
- **Docker**: Contenedorización
- **Git**: Control de versiones

## Mantenimiento y Soporte

### Logs y Monitoreo
- Los logs se almacenan en `logs/app.log`
- Nivel de logging configurable
- Monitoreo de errores y excepciones

### Backup de Base de Datos
```bash
# Backup completo
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql $DATABASE_URL < backup_file.sql
```

### Actualizaciones
1. Hacer pull de los cambios más recientes
2. Actualizar dependencias si es necesario
3. Ejecutar migraciones de base de datos
4. Reiniciar la aplicación

## Seguridad

### Validaciones
- Validación de formularios en frontend y backend
- Sanitización de datos de entrada
- Verificación de tipos de archivo para imágenes
- Protección CSRF en formularios

### Autenticación
- Sistema de sesiones seguro
- Claves secretas configuradas por entorno
- Control de acceso a rutas sensibles

### Archivos
- Validación de tipos MIME
- Límites de tamaño de archivo
- Nombres de archivo únicos y seguros
- Almacenamiento en directorios protegidos

## Rendimiento

### Optimizaciones Implementadas
- Consultas de base de datos optimizadas
- Paginación en listas grandes
- Carga lazy de imágenes
- Compresión de archivos estáticos

### Monitoreo de Rendimiento
- Tiempo de respuesta de consultas
- Uso de memoria y CPU
- Tamaño de archivos subidos
- Estadísticas de uso

## Troubleshooting

### Problemas Comunes

#### Error de conexión a base de datos
```bash
# Verificar variables de entorno
echo $DATABASE_URL

# Probar conexión
python -c "from app_modular import create_app; app = create_app(); print('OK')"
```

#### Error de permisos en directorio de uploads
```bash
# Crear directorio con permisos correctos
mkdir -p static/uploads/acciones_1000
chmod 755 static/uploads/acciones_1000
```

#### Error de validación de formulario
- Verificar que todos los campos obligatorios estén completos
- Comprobar que se haya seleccionado ubicación en el mapa
- Verificar que se hayan adjuntado fotografías

### Logs de Error
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Buscar errores específicos
grep "ERROR" logs/app.log
```

## Contacto y Soporte

Para soporte técnico o consultas sobre el sistema:

- **Desarrollador**: [Nombre del desarrollador]
- **Email**: [email@ejemplo.com]
- **Documentación**: [URL de la documentación]
- **Repositorio**: [URL del repositorio]

## Licencia

Este proyecto está desarrollado para la Alcaldía Local Santa Fe y está sujeto a los términos de licencia correspondientes.

---

**Versión**: 1.0.0  
**Última actualización**: Enero 2024  
**Compatibilidad**: Flask 2.x, Python 3.8+
