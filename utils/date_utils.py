"""
Utilidades para manejo de fechas
"""

from datetime import datetime, date
import re

def parse_date(date_string):
    """
    Parsea una fecha en formato string a objeto datetime
    
    Args:
        date_string (str): Fecha en formato string
        
    Returns:
        datetime: Objeto datetime o None si no se puede parsear
    """
    if not date_string or date_string == 'None' or date_string == '':
        return None
    
    # Intentar diferentes formatos de fecha
    formats = [
        '%Y-%m-%d',      # 2025-03-12
        '%d/%m/%Y',      # 12/03/2025
        '%m/%d/%Y',      # 03/12/2025
        '%Y-%m-%d %H:%M:%S',  # 2025-03-12 14:30:00
        '%d-%m-%Y',      # 12-03-2025
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None

def is_valid_date(date_string):
    """
    Verifica si una fecha es válida
    
    Args:
        date_string (str): Fecha en formato string
        
    Returns:
        bool: True si la fecha es válida, False en caso contrario
    """
    return parse_date(date_string) is not None

def format_date_for_display(date_obj):
    """
    Formatea una fecha para mostrar en la interfaz
    
    Args:
        date_obj (datetime): Objeto datetime
        
    Returns:
        str: Fecha formateada
    """
    if not date_obj:
        return 'N/A'
    
    return date_obj.strftime('%d/%m/%Y')

def get_days_between_dates(start_date, end_date):
    """
    Calcula los días entre dos fechas
    
    Args:
        start_date (datetime): Fecha de inicio
        end_date (datetime): Fecha de fin
        
    Returns:
        int: Número de días entre las fechas
    """
    if not start_date or not end_date:
        return 0
    
    return (end_date - start_date).days

def get_current_date():
    """
    Obtiene la fecha actual
    
    Returns:
        datetime: Fecha actual
    """
    return datetime.now()

def is_date_in_range(date_obj, start_date, end_date):
    """
    Verifica si una fecha está en un rango
    
    Args:
        date_obj (datetime): Fecha a verificar
        start_date (datetime): Fecha de inicio del rango
        end_date (datetime): Fecha de fin del rango
        
    Returns:
        bool: True si la fecha está en el rango
    """
    if not all([date_obj, start_date, end_date]):
        return False
    
    return start_date <= date_obj <= end_date 