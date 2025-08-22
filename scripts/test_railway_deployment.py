#!/usr/bin/env python3
"""
Script para diagnosticar problemas de Railway en producción
"""

import os
import sys
import json
import traceback

def check_railway_environment():
    """Verificar si estamos en Railway y qué variables están disponibles"""
    print("🔍 DIAGNÓSTICO DE RAILWAY")
    print("=" * 50)
    
    # Verificar si estamos en Railway
    railway_vars = [
        "RAILWAY_ENVIRONMENT",
        "RAILWAY_STATIC_URL", 
        "RAILWAY_PROJECT_ID",
        "RAILWAY_SERVICE_ID"
    ]
    
    print("🚂 Variables de Railway detectadas:")
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: NO CONFIGURADA")
    
    # Verificar variables críticas para San Bernardo
    print(f"\n📋 Variables críticas para San Bernardo:")
    critical_vars = {
        'SAN_BERNARDO_SHEET_ID': 'ID de la hoja de Google Sheets',
        'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON': 'Credenciales JSON de Google'
    }
    
    missing_vars = []
    for var_name, description in critical_vars.items():
        value = os.environ.get(var_name)
        if value:
            if var_name == 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON':
                try:
                    json.loads(value)
                    print(f"   ✅ {var_name}: Configurada (JSON válido)")
                except json.JSONDecodeError as e:
                    print(f"   ❌ {var_name}: JSON inválido - {e}")
                    missing_vars.append(var_name)
            else:
                print(f"   ✅ {var_name}: {value}")
        else:
            print(f"   ❌ {var_name}: NO CONFIGURADA")
            missing_vars.append(var_name)
    
    return missing_vars

def test_google_sheets_connection():
    """Probar conexión a Google Sheets"""
    print(f"\n🔌 PRUEBA DE CONEXIÓN A GOOGLE SHEETS")
    print("-" * 40)
    
    try:
        # Importar módulos necesarios
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from services.google_sheets_service import GoogleSheetsConnector
        from config import Config
        
        config = Config()
        
        print(f"📊 Configuración detectada:")
        print(f"   Sheet ID: {config.SAN_BERNARDO_SHEET_ID}")
        print(f"   Archivo credenciales: {config.SAN_BERNARDO_CREDENTIALS_FILE}")
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
            print(f"📥 Obteniendo datos del Sheet ID: {config.SAN_BERNARDO_SHEET_ID}")
            data = connector.get_data(config.SAN_BERNARDO_SHEET_ID)
            
            if data:
                print(f"✅ Datos obtenidos exitosamente: {len(data)} registros")
                return True
            else:
                print("❌ No se pudieron obtener datos")
                return False
        else:
            print("❌ Error al conectar a Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        print(f"📋 Detalles del error:")
        traceback.print_exc()
        return False

def test_flask_app():
    """Probar si la aplicación Flask puede iniciar"""
    print(f"\n🌐 PRUEBA DE APLICACIÓN FLASK")
    print("-" * 40)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Intentar importar la aplicación
        from app_modular import app
        
        print("✅ Aplicación Flask importada correctamente")
        
        # Verificar configuración
        print(f"🔧 Configuración de la app:")
        print(f"   Debug: {app.debug}")
        print(f"   Testing: {app.testing}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al importar la aplicación Flask: {e}")
        print(f"📋 Detalles del error:")
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 DIAGNÓSTICO COMPLETO DE RAILWAY")
    print("=" * 60)
    
    # 1. Verificar entorno Railway
    missing_vars = check_railway_environment()
    
    if missing_vars:
        print(f"\n❌ VARIABLES FALTANTES EN RAILWAY:")
        for var in missing_vars:
            print(f"   - {var}")
        
        print(f"\n🔧 CONFIGURACIÓN NECESARIA:")
        print("1. Ve a tu proyecto en Railway")
        print("2. Ve a la pestaña 'Variables'")
        print("3. Agrega las variables faltantes")
        
        if 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON' in missing_vars:
            print(f"\n📋 Para GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON:")
            print("   Copia todo el contenido del archivo credencials_sanbernardo.json")
        
        return False
    
    print(f"\n✅ TODAS LAS VARIABLES ESTÁN CONFIGURADAS")
    
    # 2. Probar aplicación Flask
    flask_ok = test_flask_app()
    
    # 3. Probar conexión Google Sheets
    google_ok = test_google_sheets_connection()
    
    # 4. Resumen final
    print(f"\n📊 RESUMEN DEL DIAGNÓSTICO:")
    print(f"   Flask App: {'✅ OK' if flask_ok else '❌ ERROR'}")
    print(f"   Google Sheets: {'✅ OK' if google_ok else '❌ ERROR'}")
    
    if flask_ok and google_ok:
        print(f"\n🎉 TODO FUNCIONANDO CORRECTAMENTE")
        print("La aplicación debería funcionar en Railway")
    else:
        print(f"\n⚠️ HAY PROBLEMAS QUE RESOLVER")
        if not flask_ok:
            print("   - Problema con la aplicación Flask")
        if not google_ok:
            print("   - Problema con Google Sheets")
    
    return flask_ok and google_ok

if __name__ == "__main__":
    main()
