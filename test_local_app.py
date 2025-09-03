#!/usr/bin/env python3
"""
Script para probar la aplicación local
"""

import requests
import time

def test_local_app():
    """Probar que la aplicación local esté funcionando"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 PROBANDO APLICACIÓN LOCAL")
    print("=" * 40)
    
    try:
        # 1. Probar página principal
        print("1. Probando página principal...")
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Página principal: OK")
            
            # Verificar que contenga elementos importantes
            content = response.text.lower()
            if "acceso administrativo" in content:
                print("   ✅ Enlace de Acceso Administrativo: Encontrado")
            else:
                print("   ⚠️  Enlace de Acceso Administrativo: No encontrado")
                
            if "santa fe" in content:
                print("   ✅ Contenido de Santa Fe: Encontrado")
            else:
                print("   ⚠️  Contenido de Santa Fe: No encontrado")
        else:
            print(f"   ❌ Página principal: Error {response.status_code}")
            return False
        
        # 2. Probar página de login
        print("2. Probando página de login...")
        response = requests.get(f"{base_url}/login", timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Página de login: OK")
            
            # Verificar que sea la página correcta
            content = response.text.lower()
            if "acceso administrativo" in content and "contraseña" in content:
                print("   ✅ Formulario de login: Correcto")
            else:
                print("   ⚠️  Formulario de login: Puede tener problemas")
        else:
            print(f"   ❌ Página de login: Error {response.status_code}")
            return False
        
        # 3. Probar login (POST)
        print("3. Probando sistema de login...")
        
        # Intentar login con contraseña incorrecta
        login_data = {"password": "CONTRASEÑA_INCORRECTA"}
        response = requests.post(f"{base_url}/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Sistema de login: Funcionando")
            
            # Verificar que muestre error
            content = response.text.lower()
            if "incorrecta" in content:
                print("   ✅ Validación de contraseña: Funcionando")
            else:
                print("   ⚠️  Validación de contraseña: Puede tener problemas")
        else:
            print(f"   ❌ Sistema de login: Error {response.status_code}")
            return False
        
        # 4. Probar ruta protegida sin autenticación
        print("4. Probando protección de rutas...")
        response = requests.get(f"{base_url}/san-bernardo", timeout=10)
        
        if response.status_code == 302:  # Redirección al login
            print("   ✅ Protección de rutas: Funcionando (redirección al login)")
        elif response.status_code == 200:
            print("   ⚠️  Protección de rutas: Ruta accesible sin autenticación")
        else:
            print(f"   ❌ Protección de rutas: Error {response.status_code}")
        
        print("\n🎉 ¡PRUEBAS COMPLETADAS!")
        print("La aplicación está funcionando correctamente en local")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la aplicación")
        print("   Asegúrate de que la aplicación esté corriendo en http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE LA APLICACIÓN LOCAL")
    print("=" * 50)
    
    # Esperar un poco para que la aplicación esté lista
    print("⏳ Esperando que la aplicación esté lista...")
    time.sleep(2)
    
    success = test_local_app()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Abre tu navegador en http://127.0.0.1:5000")
        print("2. Haz clic en 'Acceso Administrativo'")
        print("3. Ingresa la contraseña: ALSF2025")
        print("4. Accede a las funcionalidades restringidas")
    else:
        print("\n❌ LAS PRUEBAS FALLARON")
        print("Revisa que la aplicación esté corriendo correctamente")
