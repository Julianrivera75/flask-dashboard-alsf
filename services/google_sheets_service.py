import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Optional, Tuple, List, Dict
from config.development import DevelopmentConfig
from datetime import datetime
import json  # <-- Agregado para parsear JSON desde variable de entorno

class GoogleSheetsConnector:
    """
    Clase para manejar la conexión y obtención de datos de Google Sheets
    """
    
    def __init__(self, credentials_file: str = None, credentials_env_var: str = None):
        self.credentials_file = credentials_file or DevelopmentConfig.GOOGLE_SHEETS_CREDENTIALS_FILE
        self.credentials_env_var = credentials_env_var or "GOOGLE_CREDENTIALS_JSON"
        self.scopes = DevelopmentConfig.GOOGLE_SHEETS_SCOPES
        self.client = None
        self._cache = None
        self._last_update = None
    
    def connect(self) -> bool:
        """
        Conectar a Google Sheets usando credenciales de servicio
        """
        try:
            print(f"Intentando conectar a Google Sheets...")
            print(f"Archivo de credenciales: {self.credentials_file}")
            print(f"Scopes: {self.scopes}")
            
            # Detectar si estamos en Railway
            running_on_railway = os.environ.get("RAILWAY_STATIC_URL") or os.environ.get("RAILWAY_ENVIRONMENT")
            credentials_json = os.environ.get(self.credentials_env_var)
            if running_on_railway:
                if not credentials_json:
                    print(f"❌ ERROR: No se encontró la variable de entorno {self.credentials_env_var} en Railway. Por favor, configúrala con el JSON de credenciales.")
                    return False
                print(f"Usando credenciales desde variable de entorno {self.credentials_env_var} (Railway)")
                creds_dict = json.loads(credentials_json)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(
                    creds_dict, self.scopes
                )
            else:
                if credentials_json:
                    print(f"Usando credenciales desde variable de entorno {self.credentials_env_var}")
                    creds_dict = json.loads(credentials_json)
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(
                        creds_dict, self.scopes
                    )
                else:
                    pass
                    if not os.path.exists(self.credentials_file):
                        print(f"❌ ERROR: El archivo de credenciales no existe: {self.credentials_file}")
                        return False
                    creds = ServiceAccountCredentials.from_json_keyfile_name(
                        self.credentials_file, self.scopes
                    )
            self.client = gspread.authorize(creds)
            print(f"✅ Conexión exitosa a Google Sheets")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Google Sheets: {e}")
            return False
    
    def get_data(self, sheet_id: str = None) -> List[Dict]:
        """
        Obtener datos de Google Sheets con caché
        """
        if sheet_id is None:
            # Usar el sheet_id del archivo config.py original
            sheet_id = '1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU'
        
        data, headers = self.get_sheet_data(sheet_id)
        if data:
            self._cache = data
            self._last_update = datetime.now()
            return data
        return []
    
    def refresh_cache(self):
        """
        Refrescar el caché de datos
        """
        self._cache = None
        self._last_update = None
    
    def get_sheet_data(self, sheet_id: str) -> Tuple[Optional[List[Dict]], Optional[List[str]]]:
        """
        Obtener datos de Google Sheets
        Retorna: (datos, orden_columnas) o (None, None) si hay error
        """
        try:
            if not self.client:
                if not self.connect():
                    print("No se pudo conectar a Google Sheets")
                    return None, None
            
            # Abrir la hoja de cálculo
            sheet = self.client.open_by_key(sheet_id).sheet1
            
            # Obtener todos los valores
            all_values = sheet.get_all_values()
            
            if not all_values:
                print("La hoja está vacía")
                return None, None
            
            # La primera fila contiene los encabezados
            headers = all_values[0]
            print(f"Encabezados de la hoja: {headers}")
            # Crear lista de diccionarios con los datos
            data = []
            for row in all_values[1:]:  # Saltar la fila de encabezados
                # Asegurar que la fila tenga la misma longitud que los encabezados
                while len(row) < len(headers):
                    row.append('')
                
                # Crear diccionario con encabezados como claves
                row_dict = dict(zip(headers, row))
                data.append(row_dict)
            
            print(f"Datos obtenidos de Google Sheets: {len(data)} registros")
            return data, headers
            
        except Exception as e:
            print(f"Error obteniendo datos de Google Sheets: {e}")
            return None, None
    
    def is_connected(self) -> bool:
        """
        Verifica si hay una conexión activa
        """
        return self.client is not None 