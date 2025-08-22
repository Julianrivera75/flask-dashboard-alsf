"""
Servicio para manejo de geometría y verificación de polígonos
"""

import xml.etree.ElementTree as ET
import logging
from typing import List, Tuple, Dict, Optional
import os

logger = logging.getLogger(__name__)

class GeometryService:
    """Servicio para manejar operaciones geométricas y verificación de polígonos"""
    
    def __init__(self, kml_file_path: str = 'static/data/upz_santafe.kml'):
        self.kml_file_path = kml_file_path
        self.polygons = self._load_polygons()
    
    def _load_polygons(self) -> Dict[str, List[List[Tuple[float, float]]]]:
        """Carga los polígonos desde el archivo KML"""
        try:
            if not os.path.exists(self.kml_file_path):
                logger.error(f"Archivo KML no encontrado: {self.kml_file_path}")
                return {}
            
            tree = ET.parse(self.kml_file_path)
            root = tree.getroot()
            
            # Namespace para KML
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
            
            polygons = {}
            
            # Buscar todos los Placemarks
            for placemark in root.findall('.//kml:Placemark', ns):
                name_elem = placemark.find('kml:name', ns)
                if name_elem is not None:
                    upz_code = name_elem.text.strip()
                    
                    # Buscar las coordenadas del polígono
                    coords_elem = placemark.find('.//kml:coordinates', ns)
                    if coords_elem is not None:
                        coords_text = coords_elem.text.strip()
                        coordinates = self._parse_coordinates(coords_text)
                        
                        if coordinates:
                            polygons[upz_code] = coordinates
                            logger.info(f"Polígono cargado para UPZ {upz_code}: {len(coordinates)} puntos")
            
            logger.info(f"Total de polígonos cargados: {len(polygons)}")
            return polygons
            
        except Exception as e:
            logger.error(f"Error cargando polígonos KML: {e}")
            return {}
    
    def _parse_coordinates(self, coords_text: str) -> List[List[Tuple[float, float]]]:
        """Parsea las coordenadas del texto KML"""
        try:
            # Dividir por espacios y líneas
            coord_pairs = coords_text.split()
            
            coordinates = []
            for pair in coord_pairs:
                if pair.strip():
                    # Formato: "longitud,latitud,altitud" (altitud es opcional)
                    parts = pair.split(',')
                    if len(parts) >= 2:
                        lng = float(parts[0])
                        lat = float(parts[1])
                        coordinates.append([lng, lat])  # [longitud, latitud]
            
            return coordinates
            
        except Exception as e:
            logger.error(f"Error parseando coordenadas: {e}")
            return []
    
    def is_point_in_polygon(self, point: Tuple[float, float], polygon: List[List[float]]) -> bool:
        """
        Verifica si un punto está dentro de un polígono usando el algoritmo ray casting
        
        Args:
            point: Tupla (latitud, longitud)
            polygon: Lista de coordenadas del polígono [[lng, lat], [lng, lat], ...]
        
        Returns:
            bool: True si el punto está dentro del polígono
        """
        try:
            lat, lng = point
            
            # Convertir el punto a formato [lng, lat] para consistencia
            point_lng_lat = [lng, lat]
            
            # Implementar algoritmo ray casting
            inside = False
            j = len(polygon) - 1
            
            for i in range(len(polygon)):
                if ((polygon[i][1] > point_lng_lat[1]) != (polygon[j][1] > point_lng_lat[1]) and
                    point_lng_lat[0] < (polygon[j][0] - polygon[i][0]) * (point_lng_lat[1] - polygon[i][1]) / 
                    (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
                    inside = not inside
                j = i
            
            return inside
            
        except Exception as e:
            logger.error(f"Error verificando punto en polígono: {e}")
            return False
    
    def find_containing_upz(self, lat: float, lng: float) -> Optional[str]:
        """
        Encuentra la UPZ que contiene el punto especificado
        
        Args:
            lat: Latitud del punto
            lng: Longitud del punto
        
        Returns:
            str: Código de la UPZ que contiene el punto, o None si no está en ninguna
        """
        try:
            point = (lat, lng)
            
            for upz_code, polygon in self.polygons.items():
                if self.is_point_in_polygon(point, polygon):
                    logger.info(f"Punto ({lat}, {lng}) está en UPZ {upz_code}")
                    return upz_code
            
            logger.info(f"Punto ({lat}, {lng}) no está en ninguna UPZ de Santa Fe")
            return None
            
        except Exception as e:
            logger.error(f"Error encontrando UPZ contenedora: {e}")
            return None
    
    def get_upz_info(self, upz_code: str) -> Dict[str, str]:
        """Obtiene información de una UPZ específica"""
        upz_names = {
            '91': 'UPZ Sagrado Corazón',
            '92': 'UPZ La Macarena', 
            '93': 'UPZ Las Nieves',
            '95': 'UPZ Las Cruces',
            '96': 'UPZ Lourdes'
        }
        
        return {
            'code': upz_code,
            'name': upz_names.get(upz_code, f'UPZ {upz_code}'),
            'locality': 'Santa Fe'
        }
    
    def validate_santa_fe_location(self, lat: float, lng: float) -> Dict[str, any]:
        """
        Valida si una ubicación está dentro de la localidad de Santa Fe
        
        Args:
            lat: Latitud del punto
            lng: Longitud del punto
        
        Returns:
            Dict con información de validación
        """
        try:
            upz_code = self.find_containing_upz(lat, lng)
            
            if upz_code:
                upz_info = self.get_upz_info(upz_code)
                return {
                    'valid': True,
                    'message': f'Ubicación válida en {upz_info["name"]}',
                    'upz_code': upz_code,
                    'upz_name': upz_info['name'],
                    'locality': upz_info['locality']
                }
            else:
                return {
                    'valid': False,
                    'message': 'La ubicación no está dentro de la localidad de Santa Fe',
                    'upz_code': None,
                    'upz_name': None,
                    'locality': None
                }
                
        except Exception as e:
            logger.error(f"Error validando ubicación: {e}")
            return {
                'valid': False,
                'message': f'Error validando ubicación: {str(e)}',
                'upz_code': None,
                'upz_name': None,
                'locality': None
            }
