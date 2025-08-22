"""
Aplicación principal Flask - Versión Modular
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
import os
import logging
from datetime import datetime

# Importar módulos propios
import config
from services.google_sheets_service import GoogleSheetsConnector
from models import db, User, Responsable, TipoActividad, Entidad, Sector, Reporte, ResultadoReporte, ArchivoReporte

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

def create_app(config_class=config.DevelopmentConfig):
    """Factory function para crear la aplicación Flask"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuración para sesiones (necesario para autenticación)
    app.secret_key = 'tu_clave_secreta_super_segura_2024'
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Configuración para producción
    if app.config.get('ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    # Inicializar servicios
    sheets_connector = GoogleSheetsConnector()
    
    # Registrar blueprints
    from routes.reportes import reportes_bp
    from routes.analytics_routes import analytics_bp
    app.register_blueprint(reportes_bp)
    app.register_blueprint(analytics_bp)
    
    # Inicializar middleware de analytics
    from middleware.analytics_middleware import init_analytics_middleware
    init_analytics_middleware(app)
    
    @app.route('/')
    def index():
        """Ruta principal - Home"""
        try:
            logger.info("Accediendo a la página principal")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error en ruta principal: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/init-db')
    def init_database():
        """Ruta para inicializar la base de datos en Railway"""
        try:
            with app.app_context():
                # Crear todas las tablas
                db.create_all()
                
                # Verificar si ya hay datos
                from models import Responsable, TipoActividad, Entidad, Sector
                
                # Crear datos básicos si no existen
                if not Responsable.query.first():
                    # Crear responsables básicos
                    responsables = [
                        Responsable(nombre="Alcaldía Local Santa Fe", activo=True),
                        Responsable(nombre="Secretaría de Gobierno", activo=True),
                        Responsable(nombre="Secretaría de Seguridad", activo=True),
                        Responsable(nombre="Secretaría de Salud", activo=True),
                        Responsable(nombre="Secretaría de Integración Social", activo=True)
                    ]
                    for r in responsables:
                        db.session.add(r)
                    
                    # Crear tipos de actividad básicos
                    tipos_actividad = [
                        TipoActividad(nombre="Operativo de Seguridad", activo=True),
                        TipoActividad(nombre="Jornada de Salud", activo=True),
                        TipoActividad(nombre="Actividad Social", activo=True),
                        TipoActividad(nombre="Mantenimiento de Espacios", activo=True),
                        TipoActividad(nombre="Otro", activo=True)
                    ]
                    for t in tipos_actividad:
                        db.session.add(t)
                    
                    # Crear entidades básicas
                    entidades = [
                        Entidad(nombre="Alcaldía Mayor de Bogotá", activo=True),
                        Entidad(nombre="Policía Nacional", activo=True),
                        Entidad(nombre="Bomberos", activo=True),
                        Entidad(nombre="Secretaría de Salud", activo=True),
                        Entidad(nombre="Secretaría de Integración Social", activo=True),
                        Entidad(nombre="OTRA", activo=True)
                    ]
                    for e in entidades:
                        db.session.add(e)
                    
                    # Crear sectores básicos
                    sectores = [
                        Sector(nombre="Sector 1", activo=True),
                        Sector(nombre="Sector 2", activo=True),
                        Sector(nombre="Sector 3", activo=True)
                    ]
                    for s in sectores:
                        db.session.add(s)
                    
                    db.session.commit()
                    logger.info("Base de datos inicializada con datos básicos")
                    return jsonify({
                        'success': True,
                        'message': 'Base de datos inicializada correctamente con datos básicos'
                    })
                else:
                    logger.info("Base de datos ya contiene datos")
                    return jsonify({
                        'success': True,
                        'message': 'Base de datos ya está inicializada'
                    })
                    
        except Exception as e:
            logger.error(f"Error al inicializar base de datos: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al inicializar base de datos: {str(e)}'
            }), 500
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Ruta para autenticación"""
        if request.method == 'POST':
            password = request.form.get('password')
            if password == 'ALSF2025':  # Contraseña para acceder
                session['authenticated'] = True
                # Redirigir a la página original que el usuario estaba intentando acceder
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
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
            return redirect(url_for('login', next=request.url))
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
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            sheets_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var=config.Config.EL_CONSUELO_CREDENTIALS_ENV_VAR)
            
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
            return redirect(url_for('login', next=request.url))
        try:
            logger.info("Accediendo a la página del Convenio Interadministrativo 302")
            return render_template('pages/convenio_interadministrativo_302.html')
        except Exception as e:
            logger.error(f"Error en página del convenio: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/formulario-georeferenciado')
    def formulario_georeferenciado():
        """Ruta para el formulario georeferenciado"""
        try:
            logger.info("Accediendo al formulario georeferenciado")
            return render_template('pages/formulario_georeferenciado.html')
        except Exception as e:
            logger.error(f"Error en formulario georeferenciado: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/api/validate-location', methods=['POST'])
    def api_validate_location():
        """API para validar si una ubicación está dentro de la localidad de Santa Fe"""
        try:
            data = request.get_json()
            lat = float(data.get('lat'))
            lng = float(data.get('lng'))
            
            # Importar el servicio de geometría
            from services.geometry_service import GeometryService
            geometry_service = GeometryService()
            
            # Validar la ubicación
            validation_result = geometry_service.validate_santa_fe_location(lat, lng)
            
            logger.info(f"Validación de ubicación ({lat}, {lng}): {validation_result}")
            
            return jsonify(validation_result)
            
        except Exception as e:
            logger.error(f"Error validando ubicación: {str(e)}")
            return jsonify({
                'valid': False,
                'message': f'Error validando ubicación: {str(e)}',
                'upz_code': None,
                'upz_name': None,
                'locality': None
            }), 500
    
    # Rutas de API de datos eliminadas por no estar en uso
    
    # Rutas de gráficos eliminadas por no estar en uso
    
    # API de El Consuelo eliminada por no estar en uso
    
    @app.route('/api/el-consuelo/data')
    def api_el_consuelo_data():
        """API para obtener datos de encuestas de El Consuelo"""
        try:
            # Obtener datos reales desde Google Sheets de El Consuelo
            sheet_id = config.EL_CONSUELO_SHEET_ID
            credentials_file = config.EL_CONSUELO_CREDENTIALS_FILE
            consuelo_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var=config.EL_CONSUELO_CREDENTIALS_ENV_VAR)
            raw_data = consuelo_connector.get_data(sheet_id)
            
            return jsonify({'data': raw_data, 'total': len(raw_data)})
        except Exception as e:
            return jsonify({'error': str(e), 'data': []}), 500
    
    def process_san_bernardo_data(raw_data):
        """
        Procesa los datos de actividades de San Bernardo para adaptarlos al formato esperado por el frontend
        """
        if not raw_data:
            return []
        
        processed_data = []
        
        for row in raw_data:
            # Crear un registro adaptado con las columnas que espera el frontend
            processed_row = {}
            
            # Mapear directamente las columnas que ya existen en el Sheet de San Bernardo
            processed_row['Fecha final de ejecución'] = row.get('Fecha final de ejecución', '')
            processed_row['Población impactada'] = row.get('Población impactada ', 0)  # Notar el espacio al final
            processed_row['Entidad'] = row.get('Entidad', 'Sin especificar')
            processed_row['Descripción de los compromisos'] = row.get('Descripción de los compromisos ', '')  # Notar el espacio al final
            processed_row['Resumen de actividades'] = row.get('Resultados ( Resumen del resultado obtenido de la intervención)', '')
            
            # Mantener datos originales para referencia
            processed_row.update(row)
            
            processed_data.append(processed_row)
        
        return processed_data

    @app.route('/api/san-bernardo/data')
    def api_san_bernardo_data():
        """API para obtener datos de San Bernardo"""
        try:
            # Obtener datos desde Google Sheets de San Bernardo
            # Usando credenciales específicas de San Bernardo
            sheet_id = config.Config.SAN_BERNARDO_SHEET_ID
            credentials_file = config.Config.SAN_BERNARDO_CREDENTIALS_FILE
            san_bernardo_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var=config.Config.SAN_BERNARDO_CREDENTIALS_ENV_VAR)
            raw_data = san_bernardo_connector.get_data(sheet_id)
            
            # Procesar los datos para adaptarlos al formato esperado
            processed_data = process_san_bernardo_data(raw_data)
            
            # Agregar timestamp de última actualización
            from datetime import datetime
            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"Datos de San Bernardo procesados: {len(processed_data)} registros")
            
            return jsonify({
                'data': processed_data, 
                'total': len(processed_data),
                'last_update': last_update
            })
        except Exception as e:
            logger.error(f"Error en API de San Bernardo: {str(e)}")
            return jsonify({'error': str(e), 'data': []}), 500
    
    @app.route('/download/secretaria-gobierno-pdf')
    def download_secretaria_gobierno_pdf():
        """Descargar el PDF de la Secretaría Distrital de Gobierno"""
        try:
            pdf_path = 'static/docs/Infografiia con los ojos en los residuos.pdf'
            if os.path.exists(pdf_path):
                return send_file(pdf_path, as_attachment=True, download_name='Infografia_con_los_ojos_en_los_residuos.pdf')
            else:
                logger.error(f"Archivo PDF no encontrado: {pdf_path}")
                return jsonify({'error': 'Archivo no encontrado'}), 404
        except Exception as e:
            logger.error(f"Error al descargar PDF: {str(e)}")
            return jsonify({'error': 'Error al descargar el archivo'}), 500
    
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
    import config
    
    app = create_app(config.DevelopmentConfig)
    
    # Configuración para desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = True
    
    app.run(host='127.0.0.1', port=port, debug=debug) 