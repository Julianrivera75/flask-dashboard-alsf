import os
import requests
import json
from typing import Dict, Any, List
import logging
from datetime import datetime

class SupabaseService:
    def __init__(self):
        # Configuración de Supabase (gratuito hasta 500MB)
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.logger = logging.getLogger(__name__)
    
    def create_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo reporte en Supabase"""
        try:
            url = f"{self.supabase_url}/rest/v1/reportes"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            }
            
            # Preparar datos
            data = {
                'nombre': report_data.get('nombre'),
                'email': report_data.get('email'),
                'telefono': report_data.get('telefono'),
                'organizacion': report_data.get('organizacion'),
                'direccion': report_data.get('direccion'),
                'latitud': float(report_data.get('latitud', 0)),
                'longitud': float(report_data.get('longitud', 0)),
                'tipo_reporte': report_data.get('tipoReporte'),
                'descripcion': report_data.get('descripcion'),
                'prioridad': report_data.get('prioridad'),
                'fecha_reporte': report_data.get('fecha'),
                'hora_reporte': report_data.get('hora'),
                'fotos_urls': report_data.get('fotos_urls', []),
                'timestamp': datetime.now().isoformat(),
                'user_agent': report_data.get('user_agent'),
                'estado': 'pendiente'
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return {
                'success': True,
                'id': response.json()[0]['id'],
                'message': 'Reporte creado exitosamente'
            }
            
        except Exception as e:
            self.logger.error(f"Error creando reporte: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_reports(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtener reportes con filtros opcionales"""
        try:
            url = f"{self.supabase_url}/rest/v1/reportes"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}'
            }
            
            params = {}
            if filters:
                if filters.get('tipo_reporte'):
                    params['tipo_reporte'] = f"eq.{filters['tipo_reporte']}"
                if filters.get('prioridad'):
                    params['prioridad'] = f"eq.{filters['prioridad']}"
                if filters.get('estado'):
                    params['estado'] = f"eq.{filters['estado']}"
                if filters.get('fecha_inicio'):
                    params['fecha_reporte'] = f"gte.{filters['fecha_inicio']}"
                if filters.get('fecha_fin'):
                    params['fecha_reporte'] = f"lte.{filters['fecha_fin']}"
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error obteniendo reportes: {e}")
            return []
    
    def update_report_status(self, report_id: int, status: str) -> bool:
        """Actualizar estado de un reporte"""
        try:
            url = f"{self.supabase_url}/rest/v1/reportes?id=eq.{report_id}"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }
            
            data = {
                'estado': status,
                'fecha_actualizacion': datetime.now().isoformat()
            }
            
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error actualizando reporte: {e}")
            return False
    
    def get_reports_by_location(self, lat: float, lng: float, radius_km: float = 5) -> List[Dict[str, Any]]:
        """Obtener reportes por proximidad geográfica"""
        try:
            # Calcular bounding box aproximado
            lat_diff = radius_km / 111.0  # 1 grado ≈ 111 km
            lng_diff = radius_km / (111.0 * abs(lat))
            
            url = f"{self.supabase_url}/rest/v1/reportes"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}'
            }
            
            params = {
                'latitud': f"gte.{lat - lat_diff},lte.{lat + lat_diff}",
                'longitud': f"gte.{lng - lng_diff},lte.{lng + lng_diff}"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            reports = response.json()
            
            # Filtrar por distancia real usando fórmula de Haversine
            filtered_reports = []
            for report in reports:
                distance = self._calculate_distance(lat, lng, report['latitud'], report['longitud'])
                if distance <= radius_km:
                    report['distancia_km'] = round(distance, 2)
                    filtered_reports.append(report)
            
            return sorted(filtered_reports, key=lambda x: x['distancia_km'])
            
        except Exception as e:
            self.logger.error(f"Error obteniendo reportes por ubicación: {e}")
            return []
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calcular distancia entre dos puntos usando fórmula de Haversine"""
        import math
        
        R = 6371  # Radio de la Tierra en km
        
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de reportes"""
        try:
            url = f"{self.supabase_url}/rest/v1/reportes"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            reports = response.json()
            
            # Calcular estadísticas
            total_reports = len(reports)
            status_counts = {}
            type_counts = {}
            priority_counts = {}
            
            for report in reports:
                # Contar por estado
                status = report.get('estado', 'pendiente')
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Contar por tipo
                report_type = report.get('tipo_reporte', 'otro')
                type_counts[report_type] = type_counts.get(report_type, 0) + 1
                
                # Contar por prioridad
                priority = report.get('prioridad', 'media')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            return {
                'total_reports': total_reports,
                'status_counts': status_counts,
                'type_counts': type_counts,
                'priority_counts': priority_counts,
                'recent_reports': reports[-10:] if reports else []  # Últimos 10 reportes
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return {} 