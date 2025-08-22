from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Las tablas de asociación se definirán después de que 'db' esté disponible
# reporte_participantes = db.Table('reporte_participantes', ...)
# reporte_entidades = db.Table('reporte_entidades', ...)

def create_models(db):
    """Función para crear todos los modelos después de que 'db' esté disponible"""
    
    # Tablas de asociación
    reporte_participantes = db.Table('reporte_participantes',
        db.Column('reporte_id', db.Integer, db.ForeignKey('reportes.id'), primary_key=True),
        db.Column('responsable_id', db.Integer, db.ForeignKey('responsables.id'), primary_key=True)
    )
    
    reporte_entidades = db.Table('reporte_entidades',
        db.Column('reporte_id', db.Integer, db.ForeignKey('reportes.id'), primary_key=True),
        db.Column('entidad_id', db.Integer, db.ForeignKey('entidades.id'), primary_key=True)
    )
    
    class Responsable(db.Model):
        __tablename__ = 'responsables'
        
        id = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100), nullable=False)
        cargo = db.Column(db.String(100))
        activo = db.Column(db.Boolean, default=True)
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Responsable {self.nombre}>'

    class TipoActividad(db.Model):
        __tablename__ = 'tipos_actividad'
        
        id = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100), nullable=False)
        descripcion = db.Column(db.Text)
        activo = db.Column(db.Boolean, default=True)
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<TipoActividad {self.nombre}>'



    class Entidad(db.Model):
        __tablename__ = 'entidades'
        
        id = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100), nullable=False)
        tipo = db.Column(db.String(50))  # policía, ejército, etc.
        activo = db.Column(db.Boolean, default=True)
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Entidad {self.nombre}>'

    class Sector(db.Model):
        __tablename__ = 'sectores'
        
        id = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100), nullable=False)
        descripcion = db.Column(db.Text)
        orden = db.Column(db.Integer, default=0)
        activo = db.Column(db.Boolean, default=True)
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<Sector {self.nombre}>'

    class Reporte(db.Model):
        __tablename__ = 'reportes'
        
        id = db.Column(db.Integer, primary_key=True)
        fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        responsable_id = db.Column(db.Integer, db.ForeignKey('responsables.id'), nullable=False)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        sector_id = db.Column(db.Integer, db.ForeignKey('sectores.id'), nullable=False)

        tipo_actividad_id = db.Column(db.Integer, db.ForeignKey('tipos_actividad.id'), nullable=False)
        acompanamiento_juridico = db.Column(db.Boolean, default=False)
        observaciones = db.Column(db.Text)
        usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        estado = db.Column(db.String(20), default='activo')  # activo, inactivo, eliminado
        fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relaciones
        responsable = db.relationship('Responsable', backref='reportes')
        sector = db.relationship('Sector', backref='reportes')

        tipo_actividad = db.relationship('TipoActividad', backref='reportes')
        usuario = db.relationship('User', backref='reportes', foreign_keys=[usuario_id])
        
        # Relaciones muchos a muchos
        participantes = db.relationship('Responsable', secondary=reporte_participantes, backref='reportes_participante')
        entidades = db.relationship('Entidad', secondary=reporte_entidades, backref='reportes_entidad')
        
        # Relación uno a muchos con resultados
        resultados = db.relationship('ResultadoReporte', backref='reporte', lazy='dynamic')
        
        def __repr__(self):
            return f'<Reporte {self.id} - {self.fecha_reporte}>'

    class ResultadoReporte(db.Model):
        __tablename__ = 'resultados_reporte'
        
        id = db.Column(db.Integer, primary_key=True)
        reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False)
        cambuches_levantados = db.Column(db.Integer, default=0)
        armas_blancas_decomisadas = db.Column(db.Integer, default=0)
        armas_fuego_decomisadas = db.Column(db.Integer, default=0)
        requisas = db.Column(db.Integer, default=0)
        sellamientos_establecimientos = db.Column(db.Integer, default=0)
        sensibilizaciones = db.Column(db.Integer, default=0)
        otra_descripcion = db.Column(db.String(200))
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<ResultadoReporte {self.id} - Reporte {self.reporte_id}>'

    class ArchivoReporte(db.Model):
        __tablename__ = 'archivos_reporte'
        
        id = db.Column(db.Integer, primary_key=True)
        reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False)
        nombre_archivo = db.Column(db.String(255), nullable=False)
        ruta_archivo = db.Column(db.String(500), nullable=False)
        tipo_archivo = db.Column(db.String(20), nullable=False)  # pdf, imagen_antes, imagen_despues
        tamano = db.Column(db.Integer)  # en bytes
        fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relación
        reporte = db.relationship('Reporte', backref='archivos')
        
        def __repr__(self):
            return f'<ArchivoReporte {self.nombre_archivo}>'
    
    # Retornar todas las clases como un diccionario
    return {
        'Responsable': Responsable,
        'TipoActividad': TipoActividad,
        'Entidad': Entidad,
        'Sector': Sector,
        'Reporte': Reporte,
        'ResultadoReporte': ResultadoReporte,
        'ArchivoReporte': ArchivoReporte
    }
