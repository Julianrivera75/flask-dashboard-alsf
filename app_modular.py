"""
Aplicación principal Flask - Versión Modular
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import logging
from datetime import datetime

# Importar módulos propios
from config.development import DevelopmentConfig
from services.google_sheets_service import GoogleSheetsConnector

# Configurar logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app(config_class=DevelopmentConfig):
    """Factory function para crear la aplicación Flask"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuración para sesiones (necesario para autenticación)
    app.secret_key = 'tu_clave_secreta_super_segura_2024'
    
    # Configuración para producción
    if app.config.get('ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    # Inicializar servicios
    sheets_connector = GoogleSheetsConnector()
    
    @app.route('/')
    def index():
        """Ruta principal - Home"""
        try:
            logger.info("Accediendo a la página principal")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error en ruta principal: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Ruta para autenticación"""
        if request.method == 'POST':
            password = request.form.get('password')
            if password == 'ALFS2025*':  # Contraseña para acceder
                session['authenticated'] = True
                return redirect(url_for('san_bernardo'))
            else:
                return render_template('login.html', error='Contraseña incorrecta')
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        """Ruta para cerrar sesión"""
        session.pop('authenticated', None)
        return redirect(url_for('index'))
    
    @app.route('/san-bernardo')
    def san_bernardo():
        """Ruta para el dashboard del Barrio San Bernardo"""
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        try:
            logger.info("Accediendo al dashboard de San Bernardo")
            return render_template('pages/san_bernardo.html')
        except Exception as e:
            logger.error(f"Error en dashboard de San Bernardo: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    # Ruta de test eliminada por no ser necesaria en producción
    
    # Ruta de datos eliminada por no estar en uso
    
    @app.route('/el-consuelo')
    def el_consuelo():
        """Ruta para el dashboard del Barrio El Consuelo"""
        try:
            logger.info("Accediendo al dashboard de El Consuelo")
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            credentials_file = 'credentials/credentials_consuelo.json'
            sheets_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var="GOOGLE_CREDENTIALS_CONSUELO_JSON")
            
            try:
                raw_data = sheets_connector.get_data(sheet_id)
                if raw_data:
                    num_encuestas = len(raw_data)
                    logger.info(f"Datos obtenidos exitosamente de Google Sheets: {num_encuestas} registros")
                    return render_template('pages/el_consuelo.html', num_encuestas=num_encuestas)
                else:
                    logger.warning("No se pudieron obtener datos de Google Sheets, usando datos por defecto")
                    return render_template('pages/el_consuelo.html', num_encuestas=0)
            except Exception as sheets_error:
                logger.error(f"Error al conectar con Google Sheets: {str(sheets_error)}")
                logger.info("Usando datos por defecto debido a error de conexión")
                return render_template('pages/el_consuelo.html', num_encuestas=0)
                
        except Exception as e:
            logger.error(f"Error en dashboard de El Consuelo: {str(e)}")
            return render_template('error.html', error=str(e)), 500

    # Ruta de download eliminada por no estar en uso

    # Ruta de formulario eliminada por no estar en uso

    # Rutas de reportes eliminadas por no estar en uso
    
    @app.route('/convenio-interadministrativo-302')
    def convenio_interadministrativo_302():
        """Ruta para la página del Convenio Interadministrativo 302"""
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        try:
            logger.info("Accediendo a la página del Convenio Interadministrativo 302")
            return render_template('pages/convenio_interadministrativo_302.html')
        except Exception as e:
            logger.error(f"Error en página del convenio: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    # Rutas de API de datos eliminadas por no estar en uso
    
    # Rutas de gráficos eliminadas por no estar en uso
    
    # API de El Consuelo eliminada por no estar en uso
    
    @app.route('/api/el-consuelo/data')
    def api_el_consuelo_data():
        """API para obtener datos de encuestas de El Consuelo"""
        try:
            # Obtener datos reales desde Google Sheets de El Consuelo
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            credentials_file = 'credentials/credentials_consuelo.json'
            consuelo_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var="GOOGLE_CREDENTIALS_CONSUELO_JSON")
            raw_data = consuelo_connector.get_data(sheet_id)
            
            return jsonify({'data': raw_data, 'total': len(raw_data)})
        except Exception as e:
            return jsonify({'error': str(e), 'data': []}), 500
    
    # Rutas de GeoServer eliminadas por no estar en uso
    
    @app.errorhandler(404)
    def not_found(error):
        """Manejo de error 404"""
        logger.warning(f"Página no encontrada: {request.url}")
        return render_template('error.html', error='Página no encontrada'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejo de error 500"""
        logger.error(f"Error interno del servidor: {str(error)}")
        return render_template('error.html', error='Error interno del servidor'), 500
    
    return app

if __name__ == '__main__':
    from config.development import DevelopmentConfig
    
    app = create_app(DevelopmentConfig)
    
    # Configuración para desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = True
    
    app.run(host='127.0.0.1', port=port, debug=debug) 