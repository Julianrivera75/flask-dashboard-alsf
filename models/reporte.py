from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.user import db

class Categoria(db.Model):
    """Modelo para las categorías de reportes"""
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con reportes
    reportes = db.relationship('Reporte', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Reporte(db.Model):
    """Modelo principal para los reportes"""
    __tablename__ = 'reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campos del formulario
    actividad = db.Column(db.Text, nullable=False)
    observaciones = db.Column(db.Text)
    
    # Georreferenciación
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    direccion = db.Column(db.String(300))
    
    # Relaciones
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Estado y metadatos
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, aprobado, rechazado
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    archivos = db.relationship('ArchivoReporte', backref='reporte', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Reporte {self.id}: {self.actividad[:50]}...>'
    
    def to_dict(self):
        """Convierte el reporte a diccionario para JSON"""
        return {
            'id': self.id,
            'actividad': self.actividad,
            'observaciones': self.observaciones,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'direccion': self.direccion,
            'categoria': self.categoria.nombre if self.categoria else None,
            'estado': self.estado,
            'fecha_reporte': self.fecha_reporte.isoformat() if self.fecha_reporte else None,
            'archivos': [archivo.to_dict() for archivo in self.archivos]
        }

class ArchivoReporte(db.Model):
    """Modelo para archivos adjuntos (PDF y fotos)"""
    __tablename__ = 'archivos_reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información del archivo
    tipo_archivo = db.Column(db.String(20), nullable=False)  # 'pdf', 'foto'
    nombre_original = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    url_publica = db.Column(db.String(500))  # Para cloud storage
    
    # Metadatos
    tamaño_bytes = db.Column(db.BigInteger)
    tipo_mime = db.Column(db.String(100))
    dimensiones = db.Column(db.String(50))  # Para fotos: "1920x1080"
    orden = db.Column(db.Integer, default=0)  # Para las fotos (1, 2)
    
    # Relaciones
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ArchivoReporte {self.nombre_original}>'
    
    def to_dict(self):
        """Convierte el archivo a diccionario para JSON"""
        return {
            'id': self.id,
            'tipo_archivo': self.tipo_archivo,
            'nombre_original': self.nombre_original,
            'nombre_archivo': self.nombre_archivo,
            'url': self.url_publica or self.ruta_archivo,
            'tamaño_bytes': self.tamaño_bytes,
            'dimensiones': self.dimensiones,
            'orden': self.orden,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None
        }
