import os

class ProductionConfig:
    """Configuración para producción"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    ENV = 'production'
    DEBUG = False
    TESTING = False
    
    # Configuración de Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials/credentials.json')
    GOOGLE_SHEETS_CONSOLO_CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CONSOLO_CREDENTIALS_FILE', 'credentials/credentials_consuelo.json')
    
    # Configuración de la aplicación
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms')
    SPREADSHEET_CONSOLO_ID = os.environ.get('SPREADSHEET_CONSOLO_ID', '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms')
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'
    
    # Configuración de seguridad
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True 