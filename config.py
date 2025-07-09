import os
from datetime import datetime

class Config:
    """
    Clase de configuración centralizada para la aplicación
    """
    
    # Configuración de Google Sheets
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU')
    CREDENTIALS_FILE = 'credentials/credentials.json'
    
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