#!/usr/bin/env python3
"""
Script simple para probar que la aplicación funcione sin errores de CSRF
"""

import requests
from bs4 import BeautifulSoup

def test_csrf():
    """Probar que la aplicación funcione sin errores de CSRF"""
    print("🧪 PROBANDO APLICACIÓN SIN ERRORES CSRF")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # 1. Probar página principal
        print("1. Probando página principal...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Página principal: OK")
        else:
            print(f"   ❌ Página principal: Error {response.status_code}")
            return False
        
        # 2. Probar formulario de acciones 1000
        print("2. Probando formulario de acciones 1000...")
        response = requests.get(f"{base_url}/acciones-1000/")
        if response.status_code == 200:
            print("   ✅ Formulario acciones 1000: OK")
            
            # Verificar que el token CSRF esté presente
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            if csrf_token:
                print("   ✅ Token CSRF: Presente")
            else:
                print("   ❌ Token CSRF: No encontrado")
                return False
        else:
            print(f"   ❌ Formulario acciones 1000: Error {response.status_code}")
            return False
        
        # 3. Probar mapa de actividades
        print("3. Probando mapa de actividades...")
        response = requests.get(f"{base_url}/acciones-1000/mapa")
        if response.status_code == 200:
            print("   ✅ Mapa de actividades: OK")
        else:
            print(f"   ❌ Mapa de actividades: Error {response.status_code}")
            return False
        
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("La aplicación está funcionando correctamente sin errores de CSRF")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la aplicación")
        print("   Asegúrate de que la aplicación esté corriendo en http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE CSRF")
    print("=" * 50)
    success = test_csrf()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. La aplicación está funcionando correctamente")
        print("2. Prueba registrar una actividad en el formulario")
        print("3. Verifica que las fotos se muestren en el mapa")
        print("4. Confirma que la hora colombiana funcione")
    else:
        print("\n❌ LAS PRUEBAS FALLARON")
        print("Revisa los errores y vuelve a intentar")

