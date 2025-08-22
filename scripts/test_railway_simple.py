#!/usr/bin/env python3
"""
Script simple para probar variables de entorno en Railway
"""

import os
import json

def main():
    print("🔍 VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("=" * 50)
    
    # Verificar variables críticas
    critical_vars = {
        'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON': 'Credenciales JSON de Google',
        'SAN_BERNARDO_SHEET_ID': 'ID de la hoja de Google Sheets'
    }
    
    print("📋 Variables críticas:")
    for var_name, description in critical_vars.items():
        value = os.environ.get(var_name)
        if value:
            if var_name == 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON':
                try:
                    # Verificar que sea JSON válido
                    creds_dict = json.loads(value)
                    print(f"   ✅ {var_name}: Configurada (JSON válido)")
                    print(f"      - Project ID: {creds_dict.get('project_id', 'N/A')}")
                    print(f"      - Client Email: {creds_dict.get('client_email', 'N/A')}")
                except json.JSONDecodeError as e:
                    print(f"   ❌ {var_name}: JSON inválido - {e}")
            else:
                print(f"   ✅ {var_name}: {value}")
        else:
            print(f"   ❌ {var_name}: NO CONFIGURADA")
    
    # Verificar si estamos en Railway
    railway_vars = [
        "RAILWAY_ENVIRONMENT",
        "RAILWAY_STATIC_URL", 
        "RAILWAY_PROJECT_ID"
    ]
    
    print(f"\n🚂 Variables de Railway:")
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: NO CONFIGURADA")
    
    # Intentar conectar a Google Sheets
    print(f"\n🔌 PRUEBA DE CONEXIÓN GOOGLE SHEETS:")
    print("-" * 40)
    
    try:
        # Importar módulos
        from services.google_sheets_service import GoogleSheetsConnector
        from config import Config
        
        config = Config()
        
        print(f"📊 Configuración detectada:")
        print(f"   Sheet ID: {config.SAN_BERNARDO_SHEET_ID}")
        print(f"   Variable entorno: {config.SAN_BERNARDO_CREDENTIALS_ENV_VAR}")
        
        # Crear conector
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        print(f"\n🔌 Intentando conectar...")
        
        # Intentar conectar
        if connector.connect():
            print("✅ Conexión exitosa a Google Sheets")
            
            # Intentar obtener datos
            print(f"📥 Obteniendo datos...")
            data = connector.get_data(config.SAN_BERNARDO_SHEET_ID)
            
            if data:
                print(f"✅ Datos obtenidos: {len(data)} registros")
                print(f"   Primer registro: {list(data[0].keys()) if data else 'N/A'}")
            else:
                print("❌ No se pudieron obtener datos")
        else:
            print("❌ Error al conectar a Google Sheets")
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
