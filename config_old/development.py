# Configuración para desarrollo

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # Configuración de Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_FILE = 'credentials/credentials.json'
    GOOGLE_SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    # Configuración de la aplicación
    APP_NAME = 'Indicadores de Gestión Localidad de Santa Fe'
    APP_VERSION = '1.0.0'
    
    # Configuración de datos
    DEFAULT_SHEET_ID = 'your-sheet-id-here'
    DEFAULT_SHEET_NAME = 'Datos'
    
    # Configuración de logging
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'logs/app.log' 