import os
import webbrowser
import threading
import time
from app_modular import create_app
from config import DevelopmentConfig

# Crear la aplicación Flask
app = create_app(DevelopmentConfig)

def open_browser():
    """Abre el navegador después de un breve retraso."""
    time.sleep(2)  # Esperar 2 segundos para que el servidor se inicie
    url = "http://localhost:5000/entornos-inspiradores"
    print(f"📍 Abriendo navegador en: {url}")
    webbrowser.open_new(url)

if __name__ == '__main__':
    print("============================================================")
    print("🌱 SERVIDOR DE ENTORNOS INSPIRADORES")
    print("============================================================")
    print("🚀 Iniciando servidor Flask...")
    print(f"📍 URL: http://localhost:5000/entornos-inspiradores")
    print(f"📍 URL Principal: http://localhost:5000/")
    print("============================================================")
    print("Presiona Ctrl+C para detener el servidor")
    print("============================================================")
    
    # Iniciar el navegador en un hilo separado
    threading.Thread(target=open_browser).start()
    
    # Iniciar el servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
