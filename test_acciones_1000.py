#!/usr/bin/env python3
"""
Script de prueba para el sistema de 1000 Acciones en 1 Día
"""

import os
import sys
import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"  # Cambiar según tu configuración
TEST_DATA = {
    "nombre_responsable": "Usuario de Prueba",
    "tipo_actividad": "DANZA",
    "area_responsable": "Deportes",
    "area_otro": "",
    "personas_impactadas": 25,
    "descripcion_detallada": "Actividad de prueba para verificar el funcionamiento del sistema",
    "observaciones_adicionales": "Esta es una observación de prueba",
    "latitud": 4.7110,
    "longitud": -74.0721
}

def test_connection():
    """Probar conexión básica al servidor"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Conexión al servidor exitosa")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_form_page():
    """Probar acceso a la página del formulario"""
    try:
        response = requests.get(f"{BASE_URL}/acciones-1000/", timeout=10)
        if response.status_code == 200:
            print("✅ Página del formulario accesible")
            return True
        else:
            print(f"❌ Error al acceder al formulario: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al acceder al formulario: {e}")
        return False

def test_list_page():
    """Probar acceso a la página de lista"""
    try:
        response = requests.get(f"{BASE_URL}/acciones-1000/listar", timeout=10)
        if response.status_code == 200:
            print("✅ Página de lista accesible")
            return True
        else:
            print(f"❌ Error al acceder a la lista: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al acceder a la lista: {e}")
        return False

def test_map_page():
    """Probar acceso a la página del mapa"""
    try:
        response = requests.get(f"{BASE_URL}/acciones-1000/mapa", timeout=10)
        if response.status_code == 200:
            print("✅ Página del mapa accesible")
            return True
        else:
            print(f"❌ Error al acceder al mapa: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al acceder al mapa: {e}")
        return False

def test_api_endpoint():
    """Probar endpoint de la API"""
    try:
        response = requests.get(f"{BASE_URL}/acciones-1000/api/actividades", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "success" in data and data["success"]:
                print("✅ API endpoint funcionando correctamente")
                print(f"   - Total de actividades: {data.get('total', 0)}")
                return True
            else:
                print(f"❌ Error en respuesta de API: {data}")
                return False
        else:
            print(f"❌ Error en API endpoint: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en API endpoint: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar respuesta JSON: {e}")
        return False

def test_form_submission():
    """Probar envío del formulario (simulado)"""
    try:
        # Crear datos de prueba
        test_data = TEST_DATA.copy()
        
        # Simular envío POST (sin archivos por simplicidad)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        # Convertir datos a formato de formulario
        form_data = "&".join([f"{k}={v}" for k, v in test_data.items()])
        
        response = requests.post(
            f"{BASE_URL}/acciones-1000/submit",
            data=form_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 400, 422]:  # 400/422 son respuestas válidas para validación
            print("✅ Endpoint de envío del formulario accesible")
            return True
        else:
            print(f"❌ Error en endpoint de envío: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en endpoint de envío: {e}")
        return False

def test_static_files():
    """Probar acceso a archivos estáticos"""
    static_files = [
        "/static/css/acciones_1000.css",
        "/static/js/acciones_1000.js",
        "/static/js/acciones_1000_listar.js",
        "/static/js/acciones_1000_mapa.js"
    ]
    
    accessible_files = 0
    total_files = len(static_files)
    
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=10)
            if response.status_code == 200:
                accessible_files += 1
                print(f"✅ Archivo estático accesible: {file_path}")
            else:
                print(f"❌ Archivo estático no accesible: {file_path} ({response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al acceder a archivo estático {file_path}: {e}")
    
    if accessible_files == total_files:
        print(f"✅ Todos los archivos estáticos son accesibles ({accessible_files}/{total_files})")
        return True
    else:
        print(f"⚠️ Solo {accessible_files}/{total_files} archivos estáticos son accesibles")
        return False

def test_database_connection():
    """Probar conexión a la base de datos (requiere que la app esté corriendo)"""
    try:
        # Intentar obtener datos de la API para verificar conexión a BD
        response = requests.get(f"{BASE_URL}/acciones-1000/api/actividades", timeout=10)
        if response.status_code == 200:
            print("✅ Conexión a la base de datos verificada")
            return True
        else:
            print(f"⚠️ No se pudo verificar la conexión a la base de datos: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️ No se pudo verificar la conexión a la base de datos: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de 1000 Acciones en 1 Día")
    print("=" * 60)
    
    tests = [
        ("Conexión básica", test_connection),
        ("Página del formulario", test_form_page),
        ("Página de lista", test_list_page),
        ("Página del mapa", test_map_page),
        ("API endpoint", test_api_endpoint),
        ("Envío del formulario", test_form_submission),
        ("Archivos estáticos", test_static_files),
        ("Conexión a base de datos", test_database_connection)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Probando: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"⚠️ Prueba falló: {test_name}")
        except Exception as e:
            print(f"❌ Error en prueba {test_name}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Resumen de pruebas: {passed_tests}/{total_tests} exitosas")
    
    if passed_tests == total_tests:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar los errores anteriores.")
        return False

def show_system_info():
    """Mostrar información del sistema"""
    print("\n📋 Información del Sistema")
    print("=" * 40)
    print(f"URL base: {BASE_URL}")
    print(f"Fecha de prueba: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    
    # Verificar si la aplicación está corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("Estado de la aplicación: ✅ Ejecutándose")
        else:
            print(f"Estado de la aplicación: ⚠️ Respuesta inesperada ({response.status_code})")
    except:
        print("Estado de la aplicación: ❌ No accesible")

def main():
    """Función principal"""
    print("🧪 Sistema de Pruebas - 1000 Acciones en 1 Día")
    print("Alcaldía Local Santa Fe")
    
    # Mostrar información del sistema
    show_system_info()
    
    # Ejecutar pruebas
    success = run_all_tests()
    
    if success:
        print("\n✅ El sistema está funcionando correctamente")
        print("🎯 Puedes proceder a usar la aplicación")
    else:
        print("\n❌ Se encontraron problemas en el sistema")
        print("🔧 Revisa los errores y corrige los problemas antes de continuar")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {e}")
        sys.exit(1)
