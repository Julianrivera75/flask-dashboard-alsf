import requests
import os
import json
from typing import Dict, Any, Optional
import logging

class RailwayGeoServerService:
    def __init__(self):
        # URL del GeoServer en Railway
        self.geoserver_url = os.getenv('GEOSERVER_URL', 'https://geoserver-app.railway.app/geoserver')
        self.admin_user = os.getenv('GEOSERVER_ADMIN_USER', 'admin')
        self.admin_password = os.getenv('GEOSERVER_ADMIN_PASSWORD', 'geoserver')
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Obtener headers de autenticación"""
        import base64
        credentials = f"{self.admin_user}:{self.admin_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
    
    def get_wms_layer_url(self, workspace: str, layer: str) -> str:
        """Obtener URL de capa WMS"""
        return f"{self.geoserver_url}/wms?service=WMS&version=1.1.0&request=GetMap&layers={workspace}:{layer}&bbox=-74.2,4.5,-74.0,4.7&width=768&height=768&srs=EPSG:4326&format=image/png"
    
    def get_wfs_features(self, workspace: str, layer: str, filter: Optional[str] = None) -> Dict[str, Any]:
        """Obtener features WFS"""
        try:
            url = f"{self.geoserver_url}/wfs"
            params = {
                'service': 'WFS',
                'version': '1.0.0',
                'request': 'GetFeature',
                'typeName': f'{workspace}:{layer}'
            }
            if filter:
                params['CQL_FILTER'] = filter
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error obteniendo features WFS: {e}")
            return {"error": str(e)}
    
    def create_workspace(self, workspace_name: str) -> bool:
        """Crear workspace en GeoServer"""
        try:
            url = f"{self.geoserver_url}/rest/workspaces"
            headers = self._get_auth_headers()
            data = {"workspace": {"name": workspace_name}}
            
            response = requests.post(url, headers=headers, json=data)
            return response.status_code in [201, 409]  # 409 si ya existe
        except Exception as e:
            self.logger.error(f"Error creando workspace: {e}")
            return False
    
    def upload_shapefile(self, file_path: str, workspace: str, layer_name: str) -> bool:
        """Subir Shapefile a GeoServer"""
        try:
            # Primero crear el workspace si no existe
            self.create_workspace(workspace)
            
            url = f"{self.geoserver_url}/rest/workspaces/{workspace}/datastores/{layer_name}/file.shp"
            headers = self._get_auth_headers()
            headers['Content-Type'] = 'application/zip'
            
            with open(file_path, 'rb') as f:
                response = requests.put(url, headers=headers, data=f)
            
            return response.status_code == 201
        except Exception as e:
            self.logger.error(f"Error subiendo shapefile: {e}")
            return False
    
    def create_layer_from_geojson(self, workspace: str, layer_name: str, geojson_data: Dict[str, Any]) -> bool:
        """Crear capa desde GeoJSON"""
        try:
            # Crear workspace si no existe
            self.create_workspace(workspace)
            
            # Crear datastore
            datastore_url = f"{self.geoserver_url}/rest/workspaces/{workspace}/datastores"
            headers = self._get_auth_headers()
            
            datastore_data = {
                "dataStore": {
                    "name": layer_name,
                    "type": "GeoJSON",
                    "enabled": True
                }
            }
            
            response = requests.post(datastore_url, headers=headers, json=datastore_data)
            if response.status_code not in [201, 409]:
                return False
            
            # Subir GeoJSON
            feature_url = f"{self.geoserver_url}/rest/workspaces/{workspace}/datastores/{layer_name}/featuretypes"
            feature_data = {
                "featureType": {
                    "name": layer_name,
                    "nativeName": layer_name,
                    "enabled": True
                }
            }
            
            response = requests.post(feature_url, headers=headers, json=feature_data)
            return response.status_code == 201
        except Exception as e:
            self.logger.error(f"Error creando capa desde GeoJSON: {e}")
            return False
    
    def update_layer_style(self, workspace: str, layer_name: str, sld_content: str) -> bool:
        """Actualizar estilo de capa"""
        try:
            url = f"{self.geoserver_url}/rest/layers/{workspace}:{layer_name}"
            headers = self._get_auth_headers()
            headers['Content-Type'] = 'application/vnd.ogc.sld+xml'
            
            response = requests.put(url, headers=headers, data=sld_content)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Error actualizando estilo: {e}")
            return False
    
    def get_layer_info(self, workspace: str, layer_name: str) -> Dict[str, Any]:
        """Obtener información de una capa"""
        try:
            url = f"{self.geoserver_url}/rest/layers/{workspace}:{layer_name}"
            headers = self._get_auth_headers()
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error obteniendo información de capa: {e}")
            return {"error": str(e)}
    
    def list_layers(self, workspace: str = None) -> Dict[str, Any]:
        """Listar capas disponibles"""
        try:
            if workspace:
                url = f"{self.geoserver_url}/rest/workspaces/{workspace}/layers"
            else:
                url = f"{self.geoserver_url}/rest/layers"
            
            headers = self._get_auth_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error listando capas: {e}")
            return {"error": str(e)}
    
    def delete_layer(self, workspace: str, layer_name: str) -> bool:
        """Eliminar capa"""
        try:
            url = f"{self.geoserver_url}/rest/layers/{workspace}:{layer_name}"
            headers = self._get_auth_headers()
            
            response = requests.delete(url, headers=headers)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Error eliminando capa: {e}")
            return False 