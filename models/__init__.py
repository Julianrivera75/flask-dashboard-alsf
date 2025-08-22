from .user import User, db

# Los modelos se crearán después de que db esté disponible
from .reporte import create_models

# Crear los modelos dinámicamente
models_dict = create_models(db)

# Extraer las clases del diccionario
Responsable = models_dict['Responsable']
TipoActividad = models_dict['TipoActividad']
Entidad = models_dict['Entidad']
Sector = models_dict['Sector']
Reporte = models_dict['Reporte']
ResultadoReporte = models_dict['ResultadoReporte']
ArchivoReporte = models_dict['ArchivoReporte']

__all__ = [
    'User', 'db', 'Reporte', 'Responsable', 'TipoActividad', 
    'Entidad', 'Sector', 'ResultadoReporte', 'ArchivoReporte'
]
