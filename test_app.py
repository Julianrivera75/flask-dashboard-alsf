#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación Flask se puede importar correctamente
"""

import sys
import os

def test_imports():
    """Probar todas las importaciones necesarias"""
    print("🔍 Probando importaciones...")
    
    try:
        # Probar importación de Flask
        from flask import Flask
        print("✅ Flask importado correctamente")
        
        # Probar importación de la aplicación
        from app_modular import create_app
        print("✅ Aplicación Flask importada correctamente")
        
        # Probar creación de la aplicación
        app = create_app()
        print("✅ Aplicación Flask creada correctamente")
        
        # Probar importación de config
        import config
        print("✅ Configuración importada correctamente")
        
        # Probar importación de modelos
        from models import db
        print("✅ Base de datos importada correctamente")
        
        # Probar importación de servicios
        from services.google_sheets_service import GoogleSheetsConnector
        print("✅ Servicio de Google Sheets importado correctamente")
        
        # Probar importación de rutas
        from routes.reportes import reportes_bp
        from routes.analytics_routes import analytics_bp
        print("✅ Blueprints de rutas importados correctamente")
        
        # Probar importación de middleware
        from middleware.analytics_middleware import init_analytics_middleware
        print("✅ Middleware importado correctamente")
        
        print("\n🎉 Todas las importaciones son exitosas!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_routes():
    """Probar que las rutas están registradas"""
    print("\n🔍 Probando rutas...")
    
    try:
        from app_modular import create_app
        app = create_app()
        
        # Verificar rutas principales
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.rule)
        
        print(f"✅ Aplicación tiene {len(routes)} rutas registradas")
        
        # Verificar rutas específicas
        expected_routes = ['/', '/login', '/logout', '/el-consuelo']
        for route in expected_routes:
            if route in routes:
                print(f"✅ Ruta {route} encontrada")
            else:
                print(f"⚠️ Ruta {route} no encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando rutas: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando pruebas de la aplicación Flask...")
    
    # Probar importaciones
    imports_ok = test_imports()
    
    if imports_ok:
        # Probar rutas
        routes_ok = test_routes()
        
        if routes_ok:
            print("\n🎉 ¡Todas las pruebas pasaron! La aplicación está lista para ejecutarse.")
        else:
            print("\n⚠️ Hay problemas con las rutas.")
    else:
        print("\n❌ Hay problemas con las importaciones.")
