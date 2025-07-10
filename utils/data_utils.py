"""
Utilidades para procesamiento de datos
"""

import re
from typing import List, Dict, Any, Optional

def clean_numeric_value(value: Any) -> float:
    """
    Limpia y convierte un valor a numérico
    
    Args:
        value: Valor a convertir
        
    Returns:
        float: Valor numérico o 0.0 si no se puede convertir
    """
    if value is None:
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Remover caracteres no numéricos excepto punto y coma
        cleaned = re.sub(r'[^\d.,]', '', value)
        # Reemplazar coma por punto
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    return 0.0

def clean_text_value(value: Any) -> str:
    """
    Limpia un valor de texto
    
    Args:
        value: Valor a limpiar
        
    Returns:
        str: Texto limpio
    """
    if value is None:
        return ''
    
    if isinstance(value, str):
        return value.strip()
    
    return str(value).strip()

def validate_required_fields(data: List[Dict], required_fields: List[str]) -> Dict[str, Any]:
    """
    Valida que los datos tengan los campos requeridos, ignorando espacios extra en los nombres de columnas
    """
    validation_result = {
        'valid': True,
        'missing_fields': [],
        'invalid_records': [],
        'total_records': len(data)
    }
    
    if not data:
        validation_result['valid'] = False
        validation_result['missing_fields'] = required_fields
        return validation_result
    
    # Normalizar nombres de columnas del registro de muestra
    sample_record = data[0]
    normalized_keys = {k.strip(): k for k in sample_record.keys()}
    for field in required_fields:
        if field not in normalized_keys:
            validation_result['missing_fields'].append(field)
            validation_result['valid'] = False
    
    # Verificar registros individuales
    for i, record in enumerate(data):
        record_keys = {k.strip(): k for k in record.keys()}
        missing_in_record = []
        for field in required_fields:
            if field not in record_keys or record[record_keys.get(field, '')] in [None, '']:
                missing_in_record.append(field)
        if missing_in_record:
            validation_result['invalid_records'].append({
                'index': i,
                'missing_fields': missing_in_record
            })
    return validation_result

def aggregate_data_by_field(data: List[Dict], field: str, value_field: Optional[str] = None) -> Dict[str, Any]:
    """
    Agrupa datos por un campo específico
    
    Args:
        data: Lista de diccionarios con datos
        field: Campo por el cual agrupar
        value_field: Campo del valor a sumar (opcional)
        
    Returns:
        Dict con datos agrupados
    """
    result = {}
    
    for record in data:
        key = record.get(field, 'Sin especificar')
        
        if key not in result:
            result[key] = {
                'count': 0,
                'total_value': 0.0,
                'records': []
            }
        
        result[key]['count'] += 1
        result[key]['records'].append(record)
        
        if value_field:
            value = clean_numeric_value(record.get(value_field, 0))
            result[key]['total_value'] += value
    
    return result

def filter_data_by_date_range(data: List[Dict], date_field: str, start_date: str, end_date: str) -> List[Dict]:
    """
    Filtra datos por rango de fechas
    
    Args:
        data: Lista de diccionarios con datos
        date_field: Campo de fecha
        start_date: Fecha de inicio (YYYY-MM-DD)
        end_date: Fecha de fin (YYYY-MM-DD)
        
    Returns:
        Lista filtrada de datos
    """
    from .date_utils import parse_date, is_date_in_range
    
    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)
    
    if not start_dt or not end_dt:
        return data
    
    filtered_data = []
    
    for record in data:
        record_date = parse_date(record.get(date_field))
        if record_date and is_date_in_range(record_date, start_dt, end_dt):
            filtered_data.append(record)
    
    return filtered_data

def calculate_statistics(data: List[Dict], numeric_field: str) -> Dict[str, float]:
    """
    Calcula estadísticas básicas para un campo numérico
    
    Args:
        data: Lista de diccionarios con datos
        numeric_field: Campo numérico a analizar
        
    Returns:
        Dict con estadísticas
    """
    values = [clean_numeric_value(record.get(numeric_field, 0)) for record in data]
    values = [v for v in values if v > 0]  # Filtrar valores positivos
    
    if not values:
        return {
            'count': 0,
            'sum': 0.0,
            'average': 0.0,
            'min': 0.0,
            'max': 0.0
        }
    
    return {
        'count': len(values),
        'sum': sum(values),
        'average': sum(values) / len(values),
        'min': min(values),
        'max': max(values)
    } 