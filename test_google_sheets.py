#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a Google Sheets
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('credentials/config.env')

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.google_sheets_service import GoogleSheetsConnector

def test_google_sheets_connection():
    """Probar la conexión a Google Sheets"""
    
    print("Probando conexión a Google Sheets...")
    print("=" * 50)
    
    # Verificar archivo de credenciales
    credentials_file = 'credentials/credentials.json'
    if not os.path.exists(credentials_file):
        print(f"❌ ERROR: No se encuentra el archivo de credenciales: {credentials_file}")
        print("📋 Asegúrate de:")
        print("   1. Haber descargado el archivo JSON de Google Cloud Console")
        print("   2. Haberlo movido a la carpeta 'credentials/'")
        print("   3. Haberlo renombrado a 'credentials.json'")
        return False
    
    print(f"Archivo de credenciales encontrado: {credentials_file}")
    
    # Verificar variables de entorno
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    if not sheet_id:
        print("❌ ERROR: No se encuentra GOOGLE_SHEET_ID en config.env")
        return False
    
    print(f"Sheet ID configurado: {sheet_id}")
    
    # Probar conexión
    try:
        connector = GoogleSheetsConnector()
        
        print("Intentando conectar...")
        if connector.connect():
            print("✅ Conexión exitosa a Google Sheets API")
            
            # Probar obtención de datos
            print("🔄 Intentando obtener datos...")
            data = connector.get_data(sheet_id)
            
            if data:
                print(f"✅ Datos obtenidos exitosamente: {len(data)} registros")
                print("📊 Primeras 3 filas:")
                for i, row in enumerate(data[:3]):
                    print(f"   Fila {i+1}: {list(row.keys())}")
                return True
            else:
                print("❌ No se pudieron obtener datos de la hoja")
                return False
        else:
            print("❌ No se pudo conectar a Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def test_google_sheets_consuelo():
    """Probar la conexión a Google Sheets para El Consuelo"""
    print("\nProbando conexión a Google Sheets (El Consuelo)...")
    print("=" * 50)
    credentials_file = 'credentials/credentials_consuelo.json'
    sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'  # <--- ID REAL DE LA HOJA DE EL CONSUELO
    if not os.path.exists(credentials_file):
        print(f"ERROR: No se encuentra el archivo de credenciales: {credentials_file}")
        return False
    print(f"Archivo de credenciales encontrado: {credentials_file}")
    if not sheet_id or 'TU_ID_DE_HOJA_AQUI' in sheet_id:
        print("ERROR: Debes configurar el ID de la hoja de El Consuelo en la variable sheet_id del script.")
        return False
    print(f"Sheet ID configurado: {sheet_id}")
    try:
        connector = GoogleSheetsConnector(credentials_file=credentials_file)
        print("Intentando conectar...")
        if connector.connect():
            print("Conexión exitosa a Google Sheets API (El Consuelo)")
            print("Intentando obtener datos...")
            data = connector.get_data(sheet_id)
            if data:
                print(f"Datos obtenidos exitosamente: {len(data)} registros")
                print("Primeras 3 filas:")
                for i, row in enumerate(data[:3]):
                    print(f"   Fila {i+1}: {list(row.keys())}")
                return True
            else:
                print("No se pudieron obtener datos de la hoja de El Consuelo")
                return False
        else:
            print("No se pudo conectar a Google Sheets (El Consuelo)")
            return False
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_google_sheets_connection()
    
    if success:
        print("\n🎉 ¡Todo está configurado correctamente!")
        print("🚀 Puedes ejecutar la aplicación principal:")
        print("   python app_modular.py")
    else:
        print("\n⚠️ Hay problemas con la configuración.")
        print("🔧 Revisa los pasos anteriores.") 
    print("\n--- Prueba de conexión para El Consuelo ---")
    success_consuelo = test_google_sheets_consuelo()
    if success_consuelo:
        print("\n🎉 ¡Conexión y datos de El Consuelo OK!")
    else:
        print("\n⚠️ Problemas con la conexión o datos de El Consuelo.") 