import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from config import Config

class DataManager:
    """
    Clase para manejar el procesamiento y gestión de datos de Google Sheets
    """
    
    def __init__(self):
        self.data = None
        self.last_update = None
        self.columns_order = None
        self.homicide_reset_date = Config.HOMICIDE_RESET_DATE
        self.homicide_reset_code = Config.HOMICIDE_RESET_CODE
    
    def normalize_date(self, date_str: str) -> Optional[str]:
        """
        Normaliza diferentes formatos de fecha a formato ISO (YYYY-MM-DD)
        Maneja múltiples formatos comunes en español
        """
        if not date_str or str(date_str).strip() == '':
            return None
        
        date_str = str(date_str).strip()
        
        # Si ya es un formato ISO válido, retornarlo
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        
        # Mapeo de meses en español
        meses_es = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
            'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
        }
        
        try:
            # Formato: DD/MM/YYYY o DD-MM-YYYY
            if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$', date_str):
                if '/' in date_str:
                    day, month, year = date_str.split('/')
                else:
                    day, month, year = date_str.split('-')
                return f"{year}-{int(month):02d}-{int(day):02d}"
            
            # Formato: YYYY/MM/DD o YYYY-MM-DD
            elif re.match(r'^\d{4}[/-]\d{1,2}[/-]\d{1,2}$', date_str):
                if '/' in date_str:
                    year, month, day = date_str.split('/')
                else:
                    year, month, day = date_str.split('-')
                return f"{year}-{int(month):02d}-{int(day):02d}"
            
            # Formato: DD de Mes de YYYY (ej: "15 de marzo de 2024")
            elif re.match(r'^\d{1,2}\s+de\s+[a-zA-Záéíóúñ]+\s+de\s+\d{4}$', date_str, re.IGNORECASE):
                match = re.match(r'^(\d{1,2})\s+de\s+([a-zA-Záéíóúñ]+)\s+de\s+(\d{4})$', date_str, re.IGNORECASE)
                if match:
                    day, month_name, year = match.groups()
                    month_name = month_name.lower()
                    if month_name in meses_es:
                        month = meses_es[month_name]
                        return f"{year}-{month:02d}-{int(day):02d}"
            
            # Formato: Mes DD, YYYY (ej: "marzo 15, 2024")
            elif re.match(r'^[a-zA-Záéíóúñ]+\s+\d{1,2},\s*\d{4}$', date_str, re.IGNORECASE):
                match = re.match(r'^([a-zA-Záéíóúñ]+)\s+(\d{1,2}),\s*(\d{4})$', date_str, re.IGNORECASE)
                if match:
                    month_name, day, year = match.groups()
                    month_name = month_name.lower()
                    if month_name in meses_es:
                        month = meses_es[month_name]
                        return f"{year}-{month:02d}-{int(day):02d}"
            
            # Formato: DD Mes YYYY (ej: "15 marzo 2024")
            elif re.match(r'^\d{1,2}\s+[a-zA-Záéíóúñ]+\s+\d{4}$', date_str, re.IGNORECASE):
                match = re.match(r'^(\d{1,2})\s+([a-zA-Záéíóúñ]+)\s+(\d{4})$', date_str, re.IGNORECASE)
                if match:
                    day, month_name, year = match.groups()
                    month_name = month_name.lower()
                    if month_name in meses_es:
                        month = meses_es[month_name]
                        return f"{year}-{month:02d}-{int(day):02d}"
            
            # Formato: DD/MM/YY (año de 2 dígitos)
            elif re.match(r'^\d{1,2}/\d{1,2}/\d{2}$', date_str):
                day, month, year = date_str.split('/')
                # Asumir años 20xx para años de 2 dígitos
                full_year = f"20{year}" if int(year) < 50 else f"19{year}"
                return f"{full_year}-{int(month):02d}-{int(day):02d}"
            
            # Formato: DD.MM.YYYY (con puntos)
            elif re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
                day, month, year = date_str.split('.')
                return f"{year}-{int(month):02d}-{int(day):02d}"
            
            # Formato: DD/MM/YYYY con espacios
            elif re.match(r'^\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{4}$', date_str):
                parts = re.split(r'\s*/\s*', date_str)
                day, month, year = parts
                return f"{year}-{int(month):02d}-{int(day):02d}"
            
            # Intentar parsear con datetime.strptime para otros formatos
            else:
                # Lista de formatos comunes a intentar
                formats = [
                    '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d',
                    '%d/%m/%y', '%d-%m-%y', '%Y/%m/%d', '%Y-%m-%d',
                    '%d %B %Y', '%d %b %Y', '%B %d, %Y', '%b %d, %Y',
                    '%d.%m.%Y', '%d.%m.%y', '%Y.%m.%d'
                ]
                
                for fmt in formats:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        return parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            
            # Si no se pudo parsear, retornar None
            print(f"⚠️ No se pudo normalizar la fecha: '{date_str}'")
            return None
            
        except Exception as e:
            print(f"❌ Error normalizando fecha '{date_str}': {e}")
            return None
    
    def process_sheet_data(self, data: List[Dict]) -> List[Dict]:
        """
        Procesa los datos de la hoja y normaliza las fechas
        """
        if not data:
            return data
        
        processed_data = []
        fechas_procesadas = 0
        fechas_originales = 0
        
        for i, row in enumerate(data):
            processed_row = row.copy()
            
            # Normalizar la columna de fecha final de ejecución
            fecha_key = Config.IMPORTANT_COLUMNS['fecha_ejecucion']
            if fecha_key in processed_row:
                fecha_original = processed_row[fecha_key]
                fecha_normalizada = self.normalize_date(fecha_original)
                processed_row[fecha_key] = fecha_normalizada
                
                # Contar fechas procesadas
                if fecha_original and str(fecha_original).strip() != '':
                    fechas_originales += 1
                    if fecha_normalizada:
                        fechas_procesadas += 1
                        print(f"✅ Fecha {i+1}: '{fecha_original}' → '{fecha_normalizada}'")
                    else:
                        print(f"❌ Fecha {i+1}: '{fecha_original}' → No se pudo normalizar")
            
            processed_data.append(processed_row)
        
        print(f"\n📊 Resumen de procesamiento de fechas:")
        print(f"   Total de fechas originales: {fechas_originales}")
        print(f"   Fechas normalizadas exitosamente: {fechas_procesadas}")
        print(f"   Fechas que fallaron: {fechas_originales - fechas_procesadas}")
        
        return processed_data
    
    def update_data(self, new_data: List[Dict], columns_order: List[str]) -> bool:
        """
        Actualiza los datos y verifica si hubo cambios
        """
        processed_data = self.process_sheet_data(new_data)
        
        # Verificar si hubo cambios
        data_changed = (
            self.data != processed_data or 
            self.columns_order != columns_order
        )
        
        if data_changed:
            self.data = processed_data
            self.columns_order = columns_order
            self.last_update = datetime.now()
            print(f"Datos actualizados: {len(processed_data)} registros (cambio detectado)")
        else:
            print("No hubo cambios en los datos de Google Sheets")
        
        return data_changed
    
    def get_data(self) -> Tuple[List[Dict], List[str], Optional[datetime]]:
        """
        Retorna los datos actuales, orden de columnas y última actualización
        """
        return self.data, self.columns_order, self.last_update
    
    def get_indicators(self) -> Dict:
        """
        Calcula los indicadores principales
        """
        if not self.data:
            return {
                'total_poblacion': 0,
                'dias_sin_homicidio': 0,
                'total_actividades': 0
            }
        
        # Calcular total de población impactada
        poblacion_key = Config.IMPORTANT_COLUMNS['poblacion']
        total_poblacion = sum(
            int(row.get(poblacion_key, 0)) 
            for row in self.data 
            if row.get(poblacion_key) and str(row.get(poblacion_key)).isdigit()
        )
        
        # Calcular días sin homicidio desde el reset
        dias_sin_homicidio = (datetime.now() - self.homicide_reset_date).days
        
        # Calcular total de actividades
        total_actividades = len(self.data)
        
        return {
            'total_poblacion': total_poblacion,
            'dias_sin_homicidio': dias_sin_homicidio,
            'total_actividades': total_actividades
        }
    
    def reset_homicide_counter(self, code: str) -> bool:
        """
        Resetea el contador de días sin homicidio si el código es correcto
        """
        if code == self.homicide_reset_code:
            self.homicide_reset_date = datetime.now()
            return True
        return False
    
    def get_entity_data(self, entity: str) -> Dict:
        """
        Obtiene datos específicos de una entidad
        """
        if not self.data:
            return {}
        
        entidad_key = Config.IMPORTANT_COLUMNS['entidad']
        entity_data = [row for row in self.data if row.get(entidad_key) == entity]
        
        # Actividades con fechas válidas
        fecha_key = Config.IMPORTANT_COLUMNS['fecha_ejecucion']
        activities_with_dates = [
            row for row in entity_data 
            if row.get(fecha_key)
        ]
        
        # Actividades sin fechas
        activities_without_dates = [
            row for row in entity_data 
            if not row.get(fecha_key)
        ]
        
        return {
            'activities_with_dates': activities_with_dates,
            'activities_without_dates': activities_without_dates,
            'total_activities': len(entity_data)
        } 