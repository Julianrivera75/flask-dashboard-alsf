#!/usr/bin/env python3
"""
Script de prueba para verificar la API de San Bernardo
"""

import requests
import json
import sys

def test_san_bernardo_api():
    """Probar la API de San Bernardo"""
    
    print("🧪 Probando API de San Bernardo...")
    
    try:
        # URL de la API
        url = "http://127.0.0.1:5000/api/data"
        
        print(f"📡 Haciendo petición a: {url}")
        
        # Hacer la petición
        response = requests.get(url, timeout=30)
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            # Intentar parsear JSON
            try:
                data = response.json()
                print("✅ Respuesta JSON válida")
                print(f"📊 Total de registros: {data.get('total', 'N/A')}")
                print(f"🕒 Última actualización: {data.get('last_update', 'N/A')}")
                
                if 'data' in data and isinstance(data['data'], list):
                    print(f"📋 Datos recibidos: {len(data['data'])} registros")
                    
                    if len(data['data']) > 0:
                        print("📝 Primer registro:")
                        print(json.dumps(data['data'][0], indent=2, ensure_ascii=False))
                        
                        # Mostrar columnas disponibles
                        columns = list(data['data'][0].keys())
                        print(f"📋 Columnas disponibles ({len(columns)}):")
                        for i, col in enumerate(columns[:10], 1):  # Solo mostrar las primeras 10
                            print(f"   {i}. {col}")
                        if len(columns) > 10:
                            print(f"   ... y {len(columns) - 10} más")
                    else:
                        print("⚠️ No hay datos en la respuesta")
                else:
                    print("❌ No se encontró el campo 'data' en la respuesta")
                    print("📄 Respuesta completa:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error al parsear JSON: {e}")
                print(f"📄 Respuesta de texto: {response.text[:500]}...")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        print("💡 Asegúrate de que la aplicación esté ejecutándose en http://127.0.0.1:5000")
        
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: La petición tardó demasiado")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"📄 Tipo de error: {type(e).__name__}")

def test_san_bernardo_page():
    """Probar la página de San Bernardo"""
    
    print("\n🌐 Probando página de San Bernardo...")
    
    try:
        # URL de la página
        url = "http://127.0.0.1:5000/san-bernardo"
        
        print(f"📡 Haciendo petición a: {url}")
        
        # Hacer la petición
        response = requests.get(url, timeout=30)
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página cargada correctamente")
            print(f"📄 Tamaño de respuesta: {len(response.text)} caracteres")
            
            # Verificar si contiene elementos importantes
            content = response.text.lower()
            
            checks = [
                ("Título de la página", "san bernardo" in content),
                ("JavaScript", "script" in content),
                ("CSS", "style" in content),
                ("Función loadData", "loaddata" in content),
                ("API endpoint", "/api/data" in content)
            ]
            
            print("🔍 Verificando elementos importantes:")
            for check_name, found in checks:
                status = "✅" if found else "❌"
                print(f"   {status} {check_name}")
                
        elif response.status_code == 302:
            print("⚠️ Redirección detectada (probablemente a login)")
            print(f"📋 Location: {response.headers.get('Location', 'N/A')}")
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de San Bernardo...")
    print("=" * 50)
    
    # Probar API
    test_san_bernardo_api()
    
    # Probar página
    test_san_bernardo_page()
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")
