"""
Servicio para manejo de datos
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from utils.data_utils import clean_numeric_value, clean_text_value, validate_required_fields
from utils.date_utils import parse_date, is_valid_date

logger = logging.getLogger(__name__)

class DataService:
    """Servicio para procesamiento y validación de datos"""
    
    def __init__(self):
        self.required_fields = [
            'Entidad',
            'Actividad',
            'Fecha final de ejecución',
            'Población impactada'
        ]
    
    def process_raw_data(self, raw_data: List[Dict]) -> Dict[str, Any]:
        """
        Procesa datos crudos y los valida
        
        Args:
            raw_data: Datos crudos de Google Sheets
            
        Returns:
            Dict con datos procesados y estadísticas
        """
        try:
            # Validar campos requeridos
            validation = validate_required_fields(raw_data, self.required_fields)
            
            if not validation['valid']:
                logger.warning(f"Campos faltantes: {validation['missing_fields']}")
            
            # Procesar datos
            processed_data = []
            stats = {
                'total_records': len(raw_data),
                'valid_records': 0,
                'invalid_records': 0,
                'total_population': 0,
                'valid_dates': 0,
                'invalid_dates': 0
            }
            
            for record in raw_data:
                processed_record = self._process_record(record)
                processed_data.append(processed_record)
                
                # Actualizar estadísticas
                if processed_record['is_valid']:
                    stats['valid_records'] += 1
                    stats['total_population'] += processed_record['population_impacted']
                    
                    if processed_record['has_valid_date']:
                        stats['valid_dates'] += 1
                    else:
                        stats['invalid_dates'] += 1
                else:
                    stats['invalid_records'] += 1
            
            return {
                'data': processed_data,
                'validation': validation,
                'statistics': stats,
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error procesando datos: {str(e)}")
            raise
    
    def _process_record(self, record: Dict) -> Dict:
        """
        Procesa un registro individual
        """
        processed = {
            'original': record,
            'is_valid': True,
            'has_valid_date': False,
            'population_impacted': 0,
            'errors': []
        }
        # Normalizar claves del registro
        record_keys = {k.strip(): k for k in record.keys()}
        # Procesar población impactada
        pop_key = record_keys.get('Población impactada', None)
        population = record.get(pop_key, 0) if pop_key else 0
        processed['population_impacted'] = clean_numeric_value(population)
        # Procesar fecha
        date_key = record_keys.get('Fecha final de ejecución', None)
        date_str = record.get(date_key, '') if date_key else ''
        processed['has_valid_date'] = is_valid_date(date_str)
        # Validar campos requeridos
        for field in self.required_fields:
            key = record_keys.get(field, None)
            if not key or not record.get(key):
                processed['errors'].append(f"Campo faltante: {field}")
                processed['is_valid'] = False
        return processed
    
    def get_entity_statistics(self, data: List[Dict]) -> Dict[str, Any]:
        """
        Obtiene estadísticas por entidad
        
        Args:
            data: Datos procesados
            
        Returns:
            Dict con estadísticas por entidad
        """
        entity_stats = {}
        
        for record in data:
            entity = record['original'].get('Entidad', 'Sin especificar')
            
            if entity not in entity_stats:
                entity_stats[entity] = {
                    'activities_count': 0,
                    'total_population': 0,
                    'activities': []
                }
            
            entity_stats[entity]['activities_count'] += 1
            entity_stats[entity]['total_population'] += record['population_impacted']
            entity_stats[entity]['activities'].append({
                'activity': record['original'].get('Actividad', ''),
                'date': record['original'].get('Fecha final de ejecución', ''),
                'population': record['population_impacted']
            })
        
        return entity_stats
    
    def get_date_range_statistics(self, data: List[Dict]) -> Dict[str, Any]:
        """
        Obtiene estadísticas por rango de fechas
        
        Args:
            data: Datos procesados
            
        Returns:
            Dict con estadísticas por fecha
        """
        date_stats = {}
        
        for record in data:
            if not record['has_valid_date']:
                continue
                
            date_str = record['original'].get('Fecha final de ejecución', '')
            date_obj = parse_date(date_str)
            
            if date_obj:
                date_key = date_obj.strftime('%Y-%m')
                
                if date_key not in date_stats:
                    date_stats[date_key] = {
                        'activities_count': 0,
                        'total_population': 0,
                        'entities': set()
                    }
                
                date_stats[date_key]['activities_count'] += 1
                date_stats[date_key]['total_population'] += record['population_impacted']
                date_stats[date_key]['entities'].add(record['original'].get('Entidad', ''))
        
        # Convertir sets a listas para serialización JSON
        for date_key in date_stats:
            date_stats[date_key]['entities'] = list(date_stats[date_key]['entities'])
        
        return date_stats 