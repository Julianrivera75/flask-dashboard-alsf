"""
Modelo para la base de datos de Acciones de Residuos
Base de datos completamente independiente de las otras
Usa SQLAlchemy binds para separar de las otras bases de datos
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Index

# Importar la instancia db principal (se inicializará en app_modular.py)
# El modelo usará __bind_key__ para apuntar a la base de datos 'residuos'
from .user import db

# Lista de localidades válidas de Bogotá
LOCALIDADES_VALIDAS = [
    'Antonio Nariño',
    'Barrios Unidos',
    'Bosa',
    'Candelaria',
    'Chapinero',
    'Ciudad Bolívar',
    'Engativá',
    'Fontibón',
    'Kennedy',
    'Los Mártires',
    'Puente Aranda',
    'Rafael Uribe Uribe',
    'San Cristóbal',
    'Santa Fe',
    'Suba',
    'Sumapaz',
    'Teusaquillo',
    'Tunjuelito',
    'Usaquén',
    'Usme'
]


class AccionResiduos(db.Model):
    """
    Modelo para registrar acciones de mitigación de residuos por localidad
    Base de datos independiente para desplegar en Railway
    """
    __tablename__ = 'acciones_residuos'
    __bind_key__ = 'residuos'  # Especifica que usa el bind 'residuos'
    
    # Campos principales
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Localidad (validada contra lista de localidades válidas)
    localidad = Column(String(100), nullable=False, index=True)
    
    # Números de acciones realizadas
    numero_operativos = Column(Integer, default=0, nullable=False)
    numero_comparendos = Column(Integer, default=0, nullable=False)
    numero_sensibilizaciones = Column(Integer, default=0, nullable=False)
    
    # Fechas
    fecha_operacion = Column(Date, nullable=False, index=True)  # Fecha de la operación/reporte
    fecha_registro = Column(DateTime, default=datetime.now, nullable=False)  # Fecha de registro en sistema
    
    # Campos opcionales
    usuario_registro = Column(String(100))  # Usuario que registró
    observaciones = Column(Text)  # Notas adicionales
    
    # Timestamps automáticos
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # Índices compuestos para búsquedas rápidas
    __table_args__ = (
        Index('idx_localidad_fecha', 'localidad', 'fecha_operacion'),
    )
    
    def __repr__(self):
        return f'<AccionResiduos {self.localidad} - {self.fecha_operacion}>'
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'localidad': self.localidad,
            'numero_operativos': self.numero_operativos,
            'numero_comparendos': self.numero_comparendos,
            'numero_sensibilizaciones': self.numero_sensibilizaciones,
            'fecha_operacion': self.fecha_operacion.isoformat() if self.fecha_operacion else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'usuario_registro': self.usuario_registro,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def validar_localidad(localidad):
        """Validar que la localidad sea una de las válidas"""
        return localidad in LOCALIDADES_VALIDAS
    
    @staticmethod
    def obtener_localidades():
        """Obtener lista de localidades válidas"""
        return LOCALIDADES_VALIDAS.copy()

