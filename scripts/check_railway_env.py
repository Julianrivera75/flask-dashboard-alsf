#!/usr/bin/env python3
"""
Script para verificar las variables de entorno necesarias en Railway
"""

import os
import json
import sys

def check_railway_environment():
    """Verificar el entorno de Railway y las variables necesarias"""
    print("🔍 VERIFICACIÓN DE ENTORNO RAILWAY")
    print("=" * 50)
    
    # Verificar si estamos en Railway
    railway_env = os.environ.get("RAILWAY_ENVIRONMENT")
    railway_static_url = os.environ.get("RAILWAY_STATIC_URL")
    
    print(f"🚂 Railway Environment: {railway_env}")
    print(f"🌐 Railway Static URL: {railway_static_url}")
    
    if railway_env or railway_static_url:
        print("✅ Detectado entorno Railway")
    else:
        print("⚠️ No detectado entorno Railway (ejecutando en local)")
    
    print("\n📋 VARIABLES DE ENTORNO NECESARIAS:")
    print("-" * 40)
    
    # Variables necesarias para San Bernardo
    required_vars = {
        'SAN_BERNARDO_SHEET_ID': 'ID de la hoja de Google Sheets de San Bernardo',
        'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON': 'Credenciales JSON de Google para San Bernardo',
        'FLASK_ENV': 'Entorno de Flask (production/development)',
        'FLASK_APP': 'Aplicación Flask (wsgi.py)',
        'PORT': 'Puerto de la aplicación'
    }
    
    missing_vars = []
    
    for var_name, description in required_vars.items():
        value = os.environ.get(var_name)
        if value:
            if var_name == 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON':
                # Verificar que sea JSON válido
                try:
                    json.loads(value)
                    print(f"✅ {var_name}: Configurada (JSON válido)")
                except json.JSONDecodeError:
                    print(f"❌ {var_name}: Configurada pero JSON inválido")
                    missing_vars.append(var_name)
            else:
                print(f"✅ {var_name}: {value}")
        else:
            print(f"❌ {var_name}: NO CONFIGURADA")
            missing_vars.append(var_name)
    
    print(f"\n📊 RESUMEN:")
    print(f"   Variables configuradas: {len(required_vars) - len(missing_vars)}/{len(required_vars)}")
    
    if missing_vars:
        print(f"\n❌ VARIABLES FALTANTES:")
        for var in missing_vars:
            print(f"   - {var}")
        
        print(f"\n🔧 CONFIGURACIÓN NECESARIA EN RAILWAY:")
        print("1. Ir a tu proyecto en Railway")
        print("2. Ir a la pestaña 'Variables'")
        print("3. Agregar las siguientes variables:")
        
        for var in missing_vars:
            if var == 'SAN_BERNARDO_SHEET_ID':
                print(f"   {var} = 1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU")
            elif var == 'GOOGLE_CREDENTIALS_SAN_BERNARDO_JSON':
                print(f"   {var} = [Contenido completo del archivo credencials_sanbernardo.json]")
            elif var == 'FLASK_ENV':
                print(f"   {var} = production")
            elif var == 'FLASK_APP':
                print(f"   {var} = wsgi.py")
            elif var == 'PORT':
                print(f"   {var} = 8000")
        
        return False
    else:
        print(f"\n✅ TODAS LAS VARIABLES ESTÁN CONFIGURADAS")
        return True

def test_google_connection():
    """Probar conexión a Google Sheets"""
    print(f"\n🔌 PRUEBA DE CONEXIÓN A GOOGLE SHEETS")
    print("-" * 40)
    
    try:
        # Importar después de verificar variables
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from services.google_sheets_service import GoogleSheetsConnector
        from config import Config
        
        config = Config()
        
        # Crear conector
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        # Intentar conectar
        if connector.connect():
            print("✅ Conexión exitosa a Google Sheets")
            
            # Intentar obtener datos
            data, headers = connector.get_sheet_data(config.SAN_BERNARDO_SHEET_ID)
            if data:
                print(f"✅ Datos obtenidos: {len(data)} registros")
                return True
            else:
                print("❌ No se pudieron obtener datos")
                return False
        else:
            print("❌ Error al conectar a Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE CONFIGURACIÓN RAILWAY")
    print("=" * 60)
    
    # Verificar variables de entorno
    env_ok = check_railway_environment()
    
    if env_ok:
        # Probar conexión a Google Sheets
        connection_ok = test_google_connection()
        
        if connection_ok:
            print(f"\n🎉 TODO FUNCIONANDO CORRECTAMENTE")
            print("La aplicación debería funcionar en Railway")
        else:
            print(f"\n⚠️ PROBLEMA CON GOOGLE SHEETS")
            print("Verifica las credenciales y permisos")
    else:
        print(f"\n❌ CONFIGURACIÓN INCOMPLETA")
        print("Configura las variables faltantes en Railway")

if __name__ == "__main__":
    main()
