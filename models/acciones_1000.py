from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import pytz

def get_colombia_now():
    """Obtener la hora actual de Colombia"""
    colombia_tz = pytz.timezone('America/Bogota')
    utc_now = datetime.utcnow()
    colombia_time = colombia_tz.fromutc(utc_now)
    return colombia_time

def format_colombia_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """Formatear fecha/hora en zona horaria de Colombia"""
    if dt is None:
        return None
    
    # Si la fecha ya tiene zona horaria, convertirla
    if dt.tzinfo is not None:
        colombia_tz = pytz.timezone('America/Bogota')
        colombia_time = dt.astimezone(colombia_tz)
    else:
        # Asumir que es UTC y convertir
        utc_tz = pytz.UTC
        utc_time = utc_tz.localize(dt)
        colombia_tz = pytz.timezone('America/Bogota')
        colombia_time = utc_time.astimezone(colombia_tz)
    
    return colombia_time.strftime(format_str)

def create_acciones_1000_models(db):
    """Función para crear los modelos de 1000 acciones en 1 día"""
    
    class Actividad1000(db.Model):
        __tablename__ = 'actividades_1000'
        
        id = db.Column(db.Integer, primary_key=True)
        
        # 1. Nombre del responsable de la actividad (obligatorio)
        nombre_responsable = db.Column(db.String(200), nullable=False)
        
        # 2. Tipo de actividad (obligatorio)
        tipo_actividad = db.Column(db.String(200), nullable=False)
        
        # 3. Área responsable (obligatorio)
        area_responsable = db.Column(db.String(100), nullable=False)
        area_otro = db.Column(db.String(200))  # Campo adicional si selecciona "otro"
        
        # 4. Número de personas impactadas (obligatorio)
        personas_impactadas = db.Column(db.Integer, nullable=False)
        
        # 5. Descripción detallada (obligatorio)
        descripcion_detallada = db.Column(db.Text, nullable=False)
        
        # 6. Observaciones adicionales (opcional)
        observaciones_adicionales = db.Column(db.Text)
        
        # 7. Ubicación en el mapa (obligatorio)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        
        # 8. Fotos de la actividad (obligatorio)
        fotos = db.relationship('FotoActividad1000', backref='actividad', lazy=True, cascade='all, delete-orphan')
        
        # Campos de auditoría
        fecha_creacion = db.Column(db.DateTime, default=get_colombia_now, nullable=False)
        fecha_actualizacion = db.Column(db.DateTime, default=get_colombia_now, onupdate=get_colombia_now)
        estado = db.Column(db.String(20), default='activo')  # activo, inactivo, eliminado
        
        def __repr__(self):
            return f'<Actividad1000 {self.id}: {self.tipo_actividad}>'
        
        def to_dict(self):
            """Convertir a diccionario para JSON"""
            return {
                'id': self.id,
                'nombre_responsable': self.nombre_responsable,
                'tipo_actividad': self.tipo_actividad,
                'area_responsable': self.area_responsable,
                'area_otro': self.area_otro,
                'personas_impactadas': self.personas_impactadas,
                'descripcion_detallada': self.descripcion_detallada,
                'observaciones_adicionales': self.observaciones_adicionales,
                'latitud': self.latitud,
                'longitud': self.longitud,
                'fecha_creacion': format_colombia_time(self.fecha_creacion) if self.fecha_creacion else None,
                'estado': self.estado
            }

    class FotoActividad1000(db.Model):
        __tablename__ = 'fotos_actividades_1000'
        
        id = db.Column(db.Integer, primary_key=True)
        actividad_id = db.Column(db.Integer, db.ForeignKey('actividades_1000.id'), nullable=False)
        
        # Nombre del archivo original
        nombre_original = db.Column(db.String(255), nullable=False)
        
        # Nombre del archivo en el servidor
        nombre_archivo = db.Column(db.String(255), nullable=False)
        
        # Ruta del archivo
        ruta_archivo = db.Column(db.String(500), nullable=False)
        
        # Tipo MIME del archivo
        tipo_mime = db.Column(db.String(100))
        
        # Tamaño del archivo en bytes
        tamano_bytes = db.Column(db.BigInteger)
        
        # Fecha de subida
        fecha_subida = db.Column(db.DateTime, default=get_colombia_now, nullable=False)
        
        def __repr__(self):
            return f'<FotoActividad1000 {self.nombre_original}>'
        
        def to_dict(self):
            """Convertir a diccionario para JSON"""
            return {
                'id': self.id,
                'nombre_original': self.nombre_original,
                'nombre_archivo': self.nombre_archivo,
                'ruta_archivo': self.ruta_archivo,
                'tipo_mime': self.tipo_mime,
                'tamano_bytes': self.tamano_bytes,
                'fecha_subida': format_colombia_time(self.fecha_subida) if self.fecha_subida else None
            }

    return {
        'Actividad1000': Actividad1000,
        'FotoActividad1000': FotoActividad1000
    }
