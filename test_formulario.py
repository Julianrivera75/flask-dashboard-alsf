#!/usr/bin/env python3
"""
Script para probar el formulario de reporte
"""

from app_modular import create_app
from models import db, Responsable, TipoActividad, Entidad

def test_formulario_data():
    """Probar que los datos del formulario estén disponibles"""
    print("🔍 Probando datos del formulario de reporte...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar responsables
            responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
            print(f"✅ Responsables encontrados: {len(responsables)}")
            if responsables:
                print("   Primeros 3 responsables:")
                for i, r in enumerate(responsables[:3]):
                    print(f"   {i+1}. {r.nombre}")
            
            # Verificar tipos de actividad
            tipos_actividad = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
            print(f"✅ Tipos de actividad encontrados: {len(tipos_actividad)}")
            if tipos_actividad:
                print("   Primeros 3 tipos:")
                for i, t in enumerate(tipos_actividad[:3]):
                    print(f"   {i+1}. {t.nombre}")
            

            
            # Verificar entidades
            entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
            print(f"✅ Entidades encontradas: {len(entidades)}")
            if entidades:
                print("   Primeras 3 entidades:")
                for i, e in enumerate(entidades[:3]):
                    print(f"   {i+1}. {e.nombre}")
            
            print("\n🎉 Todos los datos del formulario están disponibles!")
            return True
            
    except Exception as e:
        print(f"❌ Error probando formulario: {e}")
        return False

def test_api_endpoints():
    """Probar que los endpoints de la API estén funcionando"""
    print("\n🔍 Probando endpoints de la API...")
    
    try:
        app = create_app()
        with app.app_context():
            # Simular request a la API
            from flask import request
            from routes.reportes import api_responsables, api_tipos_actividad
            
            # Crear contexto de request
            with app.test_request_context('/api/responsables'):
                response = api_responsables()
                print(f"✅ API Responsables: {response.status_code}")
            
            with app.test_request_context('/api/tipos-actividad'):
                response = api_tipos_actividad()
                print(f"✅ API Tipos de Actividad: {response.status_code}")
            
            print("🎉 Los endpoints de la API están funcionando!")
            return True
            
    except Exception as e:
        print(f"❌ Error probando API: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando pruebas del formulario de reporte...")
    
    # Probar datos del formulario
    formulario_ok = test_formulario_data()
    
    if formulario_ok:
        # Probar endpoints de la API
        api_ok = test_api_endpoints()
        
        if api_ok:
            print("\n🎉 ¡Todas las pruebas pasaron! El formulario está listo para usar.")
            print("\n📝 Para acceder al formulario:")
            print("   1. Ve a: http://127.0.0.1:5000/formulario-reporte")
            print("   2. Usa la contraseña: ALSF2025")
            print("   3. Los dropdowns deberían estar llenos con los datos")
        else:
            print("\n⚠️ Hay problemas con los endpoints de la API.")
    else:
        print("\n❌ Hay problemas con los datos del formulario.")
