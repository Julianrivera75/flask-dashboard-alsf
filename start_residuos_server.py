"""
Script para iniciar el servidor Flask para probar el formulario de residuos
"""
import os
import sys
from app_modular import create_app
from config import DevelopmentConfig

if __name__ == '__main__':
    print("=" * 60)
    print("SERVIDOR FLASK - FORMULARIO DE RESIDUOS")
    print("=" * 60)
    print("Iniciando servidor Flask...")
    print("URL Principal: http://localhost:5000/")
    print("URL Formulario: http://localhost:5000/acciones-residuos")
    print("=" * 60)
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        # Crear la aplicación Flask
        app = create_app(DevelopmentConfig)
        
        # Iniciar el servidor
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Desactivar reloader para evitar problemas
        )
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

