import time
from flask import request, g
from services.analytics_service import AnalyticsService

class AnalyticsMiddleware:
    """Middleware para tracking automático de analytics"""
    
    def __init__(self, app):
        self.app = app
        self.analytics_service = AnalyticsService()
        
    def __call__(self, environ, start_response):
        # Registrar tiempo de inicio
        start_time = time.time()
        
        # Procesar la request
        def custom_start_response(status, headers, exc_info=None):
            # Calcular tiempo de respuesta
            response_time = int((time.time() - start_time) * 1000)  # en milisegundos
            
            # Solo trackear páginas HTML (no API calls ni assets)
            if (environ.get('REQUEST_METHOD') == 'GET' and
                not environ.get('PATH_INFO', '').startswith('/static') and
                not environ.get('PATH_INFO', '').startswith('/api')):
                
                try:
                    # Trackear la vista de página
                    page_url = environ.get('PATH_INFO', '')
                    self.analytics_service.track_page_view(
                        page_url=page_url,
                        load_time=response_time
                    )
                except Exception as e:
                    # No fallar la request si hay error en analytics
                    print(f"Error en analytics middleware: {e}")
            
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)

def init_analytics_middleware(app):
    """Inicializar el middleware de analytics en la app Flask"""
    app.wsgi_app = AnalyticsMiddleware(app.wsgi_app)
    return app
