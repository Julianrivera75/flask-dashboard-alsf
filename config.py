import os
from datetime import datetime
from datetime import timedelta

class Config:
    """
    Clase de configuración centralizada para la aplicación
    """
    
    # Configuración de Google Sheets
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU')
    CREDENTIALS_FILE = 'credentials/credentials.json'
    
    # Configuración específica para San Bernardo
    SAN_BERNARDO_SHEET_ID = os.getenv('SAN_BERNARDO_SHEET_ID', '1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU')
    SAN_BERNARDO_CREDENTIALS_FILE = 'credentials/credencials_sanbernardo.json'
    SAN_BERNARDO_CREDENTIALS_ENV_VAR = 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON'
    
    # Configuración específica para El Consuelo
    EL_CONSUELO_SHEET_ID = os.getenv('EL_CONSUELO_SHEET_ID', '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM')
    EL_CONSUELO_CREDENTIALS_FILE = 'credentials/credentials_consuelo.json'
    EL_CONSUELO_CREDENTIALS_ENV_VAR = 'GOOGLE_CREDENTIALS_CONSUELO_JSON'
    
    # Configuración de la aplicación
    APP_NAME = "Alcaldía Mayor de Bogotá - Dashboard"
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Configuración de actualización de datos
    REFRESH_INTERVAL_HOURS = 1
    
    # Configuración de fechas
    HOMICIDE_RESET_DATE = datetime(2025, 3, 12)
    HOMICIDE_RESET_CODE = "BOGOTA2025"
    
    # Configuración de colores para gráficos
    CHART_COLORS = {
        'marzo': '#FF6B6B',
        'abril': '#4ECDC4', 
        'mayo': '#45B7D1',
        'junio': '#96CEB4',
        'julio': '#FFEAA7',
        'agosto': '#DDA0DD',
        'septiembre': '#98D8C8',
        'octubre': '#F7DC6F',
        'noviembre': '#BB8FCE',
        'diciembre': '#85C1E9',
        'alcaldia': '#FF6B6B',  # Rojo para Alcaldía
        'default': '#4ECDC4'    # Verde por defecto
    }
    
    # Configuración de columnas importantes
    IMPORTANT_COLUMNS = {
        'entidad': 'Entidad',
        'poblacion': 'Población impactada',
        'fecha_ejecucion': 'Fecha final de ejecución',
        'resumen': 'Resumen de actividades',
        'descripcion': 'Descripción de los compromisos'
    }
    
    # Configuración de scopes de Google
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ] 

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta_super_segura_2024_dev')
    
    # Forzar recarga de templates en desarrollo
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Deshabilitar caché de archivos estáticos
    
    # Base de datos independiente para acciones de residuos
    # En desarrollo usa SQLite, en producción usará PostgreSQL de Railway
    RESIDUOS_DATABASE_URI = os.environ.get('RESIDUOS_DATABASE_URL', 'sqlite:///residuos.db')
    
    # Configuración de múltiples bases de datos usando binds
    SQLALCHEMY_BINDS = {
        'residuos': os.environ.get('RESIDUOS_DATABASE_URL', 'sqlite:///residuos.db')
    }
    
    # Configuración de CSRF - Deshabilitado para sistema simple
    WTF_CSRF_ENABLED = False
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora en segundos
    WTF_CSRF_SSL_STRICT = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # Base de datos para reportes de seguridad y convivencia (nueva)
    SQLALCHEMY_DATABASE_URI = os.environ.get('REPORTES_DATABASE_URL')
    
    # Base de datos para 1000 acciones (existente en Railway)
    ACCIONES_1000_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Base de datos independiente para acciones de residuos (nueva)
    RESIDUOS_DATABASE_URI = os.environ.get('RESIDUOS_DATABASE_URL')
    
    # Configuración de múltiples bases de datos usando binds
    SQLALCHEMY_BINDS = {
        'residuos': os.environ.get('RESIDUOS_DATABASE_URL')
    }
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambiar_en_produccion_por_clave_segura')
    
    # Configuración de CSRF - Deshabilitado para mantener consistencia con sistema simple
    WTF_CSRF_ENABLED = False
    WTF_CSRF_TIME_LIMIT = 7200  # 2 horas en segundos para producción
    WTF_CSRF_SSL_STRICT = False

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 