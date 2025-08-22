#!/usr/bin/env python3
"""
Script de prueba para verificar la integración con Google Sheets de San Bernardo
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheets_service import GoogleSheetsConnector
from config import Config

# Crear instancia de configuración
config = Config()

def test_san_bernardo_connection():
    """Prueba la conexión con Google Sheets de San Bernardo"""
    print("🧪 PRUEBA DE INTEGRACIÓN SAN BERNARDO")
    print("=" * 50)
    
    # Verificar configuración
    print(f"📋 Configuración:")
    print(f"   - Sheet ID: {config.SAN_BERNARDO_SHEET_ID}")
    print(f"   - Archivo de credenciales: {config.SAN_BERNARDO_CREDENTIALS_FILE}")
    print(f"   - Variable de entorno: {config.SAN_BERNARDO_CREDENTIALS_ENV_VAR}")
    print()
    
    # Verificar archivo de credenciales
    if os.path.exists(config.SAN_BERNARDO_CREDENTIALS_FILE):
        print(f"✅ Archivo de credenciales encontrado: {config.SAN_BERNARDO_CREDENTIALS_FILE}")
        try:
            with open(config.SAN_BERNARDO_CREDENTIALS_FILE, 'r') as f:
                creds_data = json.load(f)
            print(f"   - Tipo de cuenta: {creds_data.get('type', 'N/A')}")
            print(f"   - Project ID: {creds_data.get('project_id', 'N/A')}")
            print(f"   - Client Email: {creds_data.get('client_email', 'N/A')}")
        except Exception as e:
            print(f"❌ Error al leer credenciales: {e}")
            return False
    else:
        print(f"❌ Archivo de credenciales no encontrado: {config.SAN_BERNARDO_CREDENTIALS_FILE}")
        return False
    
    print()
    
    # Verificar variable de entorno
    env_creds = os.environ.get(config.SAN_BERNARDO_CREDENTIALS_ENV_VAR)
    if env_creds:
        print(f"✅ Variable de entorno encontrada: {config.SAN_BERNARDO_CREDENTIALS_ENV_VAR}")
    else:
        print(f"⚠️ Variable de entorno no encontrada: {config.SAN_BERNARDO_CREDENTIALS_ENV_VAR}")
        print("   (Se usará el archivo local)")
    
    print()
    
    # Probar conexión
    print("🔌 Probando conexión con Google Sheets...")
    try:
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        if connector.connect():
            print("✅ Conexión exitosa con Google Sheets")
        else:
            print("❌ Error al conectar con Google Sheets")
            return False
        
        print()
        
        # Probar obtención de datos
        print("📊 Probando obtención de datos...")
        data, headers = connector.get_sheet_data(config.SAN_BERNARDO_SHEET_ID)
        
        if data is not None:
            print(f"✅ Datos obtenidos exitosamente")
            print(f"   - Total de registros: {len(data)}")
            print(f"   - Columnas: {len(headers)}")
            print(f"   - Encabezados: {headers[:5]}...")  # Mostrar solo los primeros 5
            
            if data:
                print(f"   - Primer registro: {dict(list(data[0].items())[:3])}...")  # Mostrar solo las primeras 3 columnas
        else:
            print("❌ No se pudieron obtener datos")
            return False
        
        print()
        print("🎉 PRUEBA EXITOSA - Integración funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_processing():
    """Prueba el procesamiento de datos"""
    print("\n🔧 PRUEBA DE PROCESAMIENTO DE DATOS")
    print("=" * 50)
    
    try:
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        if not connector.connect():
            print("❌ No se pudo conectar para procesar datos")
            return False
        
        # Obtener datos
        data, headers = connector.get_sheet_data(config.SAN_BERNARDO_SHEET_ID)
        
        if not data:
            print("❌ No hay datos para procesar")
            return False
        
        # Simular procesamiento básico
        print(f"📈 Procesando {len(data)} registros...")
        
        # Contar registros por tipo (ejemplo)
        tipos_encuesta = {}
        for row in data:
            # Buscar columna que pueda contener el tipo de encuesta
            tipo = None
            for key, value in row.items():
                if 'tipo' in key.lower() or 'encuesta' in key.lower():
                    tipo = value
                    break
            
            if tipo:
                tipos_encuesta[tipo] = tipos_encuesta.get(tipo, 0) + 1
            else:
                tipos_encuesta['Sin tipo'] = tipos_encuesta.get('Sin tipo', 0) + 1
        
        print("📊 Resumen de datos:")
        for tipo, cantidad in tipos_encuesta.items():
            print(f"   - {tipo}: {cantidad}")
        
        print("✅ Procesamiento de datos exitoso")
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento: {e}")
        return False

def main():
    """Función principal"""
    print(f"🚀 Iniciando pruebas de integración - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Prueba de conexión
    connection_success = test_san_bernardo_connection()
    
    if connection_success:
        # Prueba de procesamiento
        processing_success = test_data_processing()
        
        if processing_success:
            print("\n🎯 RESULTADO FINAL: Todas las pruebas pasaron exitosamente")
            print("   La integración con Google Sheets de San Bernardo está funcionando correctamente")
            return 0
        else:
            print("\n⚠️ RESULTADO FINAL: Conexión exitosa pero problemas en procesamiento")
            return 1
    else:
        print("\n❌ RESULTADO FINAL: Falló la conexión con Google Sheets")
        print("   Revisa la configuración y las credenciales")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
