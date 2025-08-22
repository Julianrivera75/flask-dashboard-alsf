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
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            consuelo_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var=config.Config.EL_CONSUELO_CREDENTIALS_ENV_VAR)
            raw_data = consuelo_connector.get_data(sheet_id)
            
            logger.info(f"Datos de El Consuelo obtenidos: {len(raw_data) if raw_data else 0} registros")
            
            return jsonify({'data': raw_data, 'total': len(raw_data) if raw_data else 0})
        except Exception as e:
            logger.error(f"Error en API de El Consuelo: {str(e)}")
            return jsonify({'error': str(e), 'data': []}), 500
    
    @app.route('/test-el-consuelo')
    def test_el_consuelo():
        """Ruta de prueba para diagnosticar problemas con El Consuelo"""
        try:
            logger.info("🧪 Iniciando prueba de El Consuelo...")
            
            # Verificar configuración
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            credentials_env_var = config.Config.EL_CONSUELO_CREDENTIALS_ENV_VAR
            
            logger.info(f"📋 Configuración El Consuelo:")
            logger.info(f"   - Sheet ID: {sheet_id}")
            logger.info(f"   - Credentials File: {credentials_file}")
            logger.info(f"   - Credentials Env Var: {credentials_env_var}")
            
            # Verificar si el archivo existe
            import os
            file_exists = os.path.exists(credentials_file)
            env_var_exists = os.environ.get(credentials_env_var) is not None
            
            logger.info(f"   - Archivo existe: {file_exists}")
            logger.info(f"   - Variable de entorno existe: {env_var_exists}")
            
            # Intentar conectar
            consuelo_connector = GoogleSheetsConnector(
                credentials_file=credentials_file, 
                credentials_env_var=credentials_env_var
            )
            
            if consuelo_connector.connect():
                logger.info("✅ Conexión exitosa a Google Sheets")
                
                # Intentar obtener datos paso a paso
                logger.info("📊 Intentando obtener datos paso a paso...")
                
                # 1. Obtener datos crudos
                raw_data, headers = consuelo_connector.get_sheet_data(sheet_id)
                logger.info(f"📊 Datos crudos obtenidos: {len(raw_data) if raw_data else 0} registros")
                logger.info(f"📋 Headers obtenidos: {headers}")
                
                if raw_data and len(raw_data) > 0:
                    logger.info(f"📋 Primer registro: {raw_data[0]}")
                    logger.info(f"📋 Último registro: {raw_data[-1]}")
                    
                    # 2. Procesar datos (simular el procesamiento real)
                    processed_data = []
                    for i, row in enumerate(raw_data[:5]):  # Solo los primeros 5 para debug
                        processed_row = {}
                        for key, value in row.items():
                            if key and value:  # Solo campos no vacíos
                                processed_row[key] = value
                        processed_data.append(processed_row)
                        logger.info(f"📋 Registro procesado {i+1}: {len(processed_row)} campos")
                    
                    # 3. Verificar si hay datos válidos
                    valid_data = [row for row in raw_data if any(row.values())]
                    logger.info(f"📊 Datos válidos (con al menos un campo): {len(valid_data)}")
                    
                    # 4. Contar campos por registro
                    if raw_data:
                        field_counts = [len([v for v in row.values() if v]) for row in raw_data]
                        avg_fields = sum(field_counts) / len(field_counts) if field_counts else 0
                        logger.info(f"📊 Promedio de campos por registro: {avg_fields:.1f}")
                        logger.info(f"📊 Mínimo campos: {min(field_counts) if field_counts else 0}")
                        logger.info(f"📊 Máximo campos: {max(field_counts) if field_counts else 0}")
                
                return jsonify({
                    'success': True,
                    'config': {
                        'sheet_id': sheet_id,
                        'credentials_file': credentials_file,
                        'credentials_env_var': credentials_env_var,
                        'file_exists': file_exists,
                        'env_var_exists': env_var_exists
                    },
                    'connection': 'success',
                    'raw_data_count': len(raw_data) if raw_data else 0,
                    'headers': headers,
                    'valid_data_count': len([row for row in (raw_data or []) if any(row.values())]),
                    'sample_data': raw_data[0] if raw_data else None,
                    'sample_processed': processed_data if 'processed_data' in locals() else None,
                    'field_stats': {
                        'avg_fields': sum([len([v for v in row.values() if v]) for row in (raw_data or [])]) / len(raw_data) if raw_data else 0,
                        'min_fields': min([len([v for v in row.values() if v]) for row in (raw_data or [])]) if raw_data else 0,
                        'max_fields': max([len([v for v in row.values() if v]) for row in (raw_data or [])]) if raw_data else 0
                    } if raw_data else None
                })
            else:
                logger.error("❌ No se pudo conectar a Google Sheets")
                return jsonify({
                    'success': False,
                    'error': 'No se pudo conectar a Google Sheets',
                    'config': {
                        'sheet_id': sheet_id,
                        'credentials_file': credentials_file,
                        'credentials_env_var': credentials_env_var,
                        'file_exists': file_exists,
                        'env_var_exists': env_var_exists
                    }
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error en prueba de El Consuelo: {str(e)}")
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
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
            
            # NO mantener datos originales para evitar duplicación
            # processed_row.update(row)  # Esta línea estaba causando duplicación
            
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

    @app.route('/test-el-consuelo-api')
    def test_el_consuelo_api():
        """Ruta de prueba que simula exactamente la API principal de El Consuelo"""
        try:
            logger.info("🧪 Probando API principal de El Consuelo...")
            
            # Simular exactamente lo que hace la API principal
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            credentials_env_var = config.Config.EL_CONSUELO_CREDENTIALS_ENV_VAR
            
            logger.info(f"📋 Usando configuración: Sheet ID {sheet_id}")
            
            consuelo_connector = GoogleSheetsConnector(
                credentials_file=credentials_file, 
                credentials_env_var=credentials_env_var
            )
            
            # Usar el método get_data() que es el que usa la API principal
            raw_data = consuelo_connector.get_data(sheet_id)
            
            logger.info(f"📊 API principal - Datos obtenidos: {len(raw_data) if raw_data else 0} registros")
            
            # Simular el procesamiento que se hace en el frontend
            if raw_data and len(raw_data) > 0:
                # Contar encuestas (asumiendo que cada fila es una encuesta)
                total_encuestas = len(raw_data)
                
                # Verificar estructura de datos
                sample_record = raw_data[0]
                logger.info(f"📋 Muestra del primer registro: {sample_record}")
                
                # Verificar si hay campos importantes
                important_fields = ['Entidad', 'Población impactada', 'Fecha final de ejecución', 'Resumen de actividades']
                available_fields = [field for field in important_fields if any(field in str(record) for record in raw_data[:5])]
                
                return jsonify({
                    'success': True,
                    'api_method': 'get_data()',
                    'total_encuestas': total_encuestas,
                    'data': raw_data,
                    'sample_record': sample_record,
                    'available_important_fields': available_fields,
                    'all_fields': list(sample_record.keys()) if sample_record else [],
                    'message': f'API principal funcionando: {total_encuestas} encuestas encontradas'
                })
            else:
                return jsonify({
                    'success': False,
                    'api_method': 'get_data()',
                    'total_encuestas': 0,
                    'data': [],
                    'error': 'No se obtuvieron datos de la API principal'
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error en prueba de API principal: {str(e)}")
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500 

    @app.route('/test-simple-consuelo')
    def test_simple_consuelo():
        """Prueba súper simple: solo abrir la hoja y contar filas"""
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            logger.info("🧪 Prueba súper simple de El Consuelo...")
            
            # Configuración
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            
            logger.info(f"📋 Sheet ID: {sheet_id}")
            logger.info(f"📁 Credentials: {credentials_file}")
            
            # Conectar directamente
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
            client = gspread.authorize(creds)
            
            logger.info("✅ Conectado a Google Sheets")
            
            # Abrir la hoja
            try:
                sheet = client.open_by_key(sheet_id)
                logger.info(f"✅ Hoja abierta: {sheet.title}")
                
                # Obtener la primera hoja
                worksheet = sheet.sheet1
                logger.info(f"✅ Primera hoja: {worksheet.title}")
                
                # Contar filas
                all_values = worksheet.get_all_values()
                total_rows = len(all_values)
                total_columns = len(all_values[0]) if all_values else 0
                
                logger.info(f"📊 Total filas: {total_rows}")
                logger.info(f"📊 Total columnas: {total_columns}")
                
                if all_values:
                    headers = all_values[0]
                    logger.info(f"📋 Headers: {headers}")
                    
                    # Contar filas con datos (no vacías)
                    non_empty_rows = [row for row in all_values[1:] if any(cell.strip() for cell in row)]
                    logger.info(f"📊 Filas con datos: {len(non_empty_rows)}")
                    
                    # Mostrar primera fila de datos
                    if non_empty_rows:
                        first_data_row = non_empty_rows[0]
                        logger.info(f"📋 Primera fila de datos: {first_data_row}")
                
                return jsonify({
                    'success': True,
                    'sheet_title': sheet.title,
                    'worksheet_title': worksheet.title,
                    'total_rows': total_rows,
                    'total_columns': total_columns,
                    'data_rows': len(non_empty_rows) if 'non_empty_rows' in locals() else 0,
                    'headers': headers if 'headers' in locals() else [],
                    'first_data_row': first_data_row if 'first_data_row' in locals() else None
                })
                
            except Exception as sheet_error:
                logger.error(f"❌ Error abriendo la hoja: {str(sheet_error)}")
                return jsonify({
                    'success': False,
                    'error': f'Error abriendo hoja: {str(sheet_error)}',
                    'sheet_id': sheet_id
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error en prueba simple: {str(e)}")
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500 

    @app.route('/verify-439-consuelo')
    def verify_439_consuelo():
        """Verificar específicamente si hay 439 registros en El Consuelo"""
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            logger.info("🔍 Verificando específicamente los 439 registros de El Consuelo...")
            
            # Configuración específica de El Consuelo
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            credentials_file = config.Config.EL_CONSUELO_CREDENTIALS_FILE
            
            logger.info(f"📋 Sheet ID de El Consuelo: {sheet_id}")
            logger.info(f"📁 Credenciales de El Consuelo: {credentials_file}")
            
            # Conectar usando las credenciales de El Consuelo
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
            client = gspread.authorize(creds)
            
            logger.info("✅ Conectado usando credenciales de El Consuelo")
            
            # Abrir la hoja específica de El Consuelo
            sheet = client.open_by_key(sheet_id)
            logger.info(f"✅ Hoja de El Consuelo abierta: {sheet.title}")
            
            # Obtener la primera hoja
            worksheet = sheet.sheet1
            logger.info(f"✅ Primera hoja: {worksheet.title}")
            
            # Obtener todos los valores
            all_values = worksheet.get_all_values()
            total_rows = len(all_values)
            
            logger.info(f"📊 Total de filas en la hoja: {total_rows}")
            
            if total_rows > 0:
                headers = all_values[0]
                data_rows = all_values[1:]  # Excluir headers
                
                # Contar filas con datos (no completamente vacías)
                non_empty_rows = [row for row in data_rows if any(cell.strip() for cell in row)]
                empty_rows = [row for row in data_rows if not any(cell.strip() for cell in row)]
                
                logger.info(f"📊 Filas con datos: {len(non_empty_rows)}")
                logger.info(f"📊 Filas vacías: {len(empty_rows)}")
                logger.info(f"📊 Headers: {len(headers)} columnas")
                
                # Verificar si hay exactamente 439 registros
                expected_count = 439
                actual_count = len(non_empty_rows)
                
                if actual_count == expected_count:
                    logger.info(f"✅ ¡EXACTO! Encontrados {actual_count} registros (esperados {expected_count})")
                    status = "EXACTO"
                elif actual_count > expected_count:
                    logger.info(f"⚠️ Más registros de lo esperado: {actual_count} (esperados {expected_count})")
                    status = "MÁS_REGISTROS"
                else:
                    logger.info(f"❌ Menos registros de lo esperado: {actual_count} (esperados {expected_count})")
                    status = "MENOS_REGISTROS"
                
                # Mostrar muestra de datos
                sample_data = []
                for i, row in enumerate(non_empty_rows[:5]):  # Primeros 5 registros
                    row_dict = dict(zip(headers, row))
                    sample_data.append({
                        'row_number': i + 1,
                        'data': row_dict
                    })
                
                return jsonify({
                    'success': True,
                    'sheet_title': sheet.title,
                    'worksheet_title': worksheet.title,
                    'expected_records': expected_count,
                    'actual_records': actual_count,
                    'total_rows_in_sheet': total_rows,
                    'headers_count': len(headers),
                    'empty_rows': len(empty_rows),
                    'status': status,
                    'headers': headers,
                    'sample_data': sample_data,
                    'message': f'Encontrados {actual_count} registros de {expected_count} esperados'
                })
            else:
                logger.warning("⚠️ La hoja está completamente vacía")
                return jsonify({
                    'success': False,
                    'error': 'La hoja está completamente vacía',
                    'total_rows': 0,
                    'expected_records': 439
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error verificando 439 registros: {str(e)}")
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'expected_records': 439
            }), 500 

    @app.route('/api/el-consuelo/data-correct')
    def api_el_consuelo_data_correct():
        """API para obtener datos de El Consuelo usando las credenciales correctas"""
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            logger.info("🔄 Obteniendo datos de El Consuelo con credenciales correctas...")
            
            # Usar las credenciales específicas que funcionan
            credentials_file = 'credentials/alcaldialocalsantafe-8a418c83a2a4.json'
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            
            logger.info(f"📁 Credenciales: {credentials_file}")
            logger.info(f"📋 Sheet ID: {sheet_id}")
            
            # Conectar directamente usando las credenciales correctas
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
            client = gspread.authorize(creds)
            
            logger.info("✅ Conectado usando credenciales correctas")
            
            # Abrir la hoja específica
            sheet = client.open_by_key(sheet_id)
            worksheet = sheet.sheet1
            
            logger.info(f"✅ Hoja abierta: {sheet.title}")
            logger.info(f"✅ Primera hoja: {worksheet.title}")
            
            # Obtener todos los valores
            all_values = worksheet.get_all_values()
            total_rows = len(all_values)
            
            logger.info(f"📊 Total de filas en la hoja: {total_rows}")
            
            if total_rows > 1:  # Más de 1 porque la primera fila son headers
                headers = all_values[0]
                data_rows = all_values[1:]  # Excluir headers
                
                # Contar filas con datos (no completamente vacías)
                non_empty_rows = [row for row in data_rows if any(cell.strip() for cell in row)]
                
                logger.info(f"📊 Filas con datos: {len(non_empty_rows)}")
                logger.info(f"📊 Headers: {len(headers)} columnas")
                
                # Crear lista de diccionarios con los datos
                data = []
                for row in non_empty_rows:
                    # Asegurar que la fila tenga la misma longitud que los headers
                    while len(row) < len(headers):
                        row.append('')
                    
                    # Crear diccionario con headers como claves
                    row_dict = dict(zip(headers, row))
                    data.append(row_dict)
                
                logger.info(f"✅ Datos procesados: {len(data)} registros")
                
                return jsonify({
                    'data': data, 
                    'total': len(data),
                    'success': True,
                    'message': f'Datos obtenidos usando credenciales correctas: {len(data)} registros'
                })
            else:
                logger.warning("⚠️ La hoja está vacía o solo tiene headers")
                return jsonify({
                    'data': [], 
                    'total': 0,
                    'success': False,
                    'error': 'La hoja está vacía o solo tiene headers'
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos de El Consuelo: {str(e)}")
            import traceback
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'data': [],
                'success': False
            }), 500 

    @app.route('/test-credentials-simple')
    def test_credentials_simple():
        """Prueba súper simple de las credenciales alcaldialocalsantafe-8a418c83a2a4.json"""
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            import os
            
            logger.info("🧪 Prueba súper simple de credenciales...")
            
            # Verificar que el archivo existe
            credentials_file = 'credentials/alcaldialocalsantafe-8a418c83a2a4.json'
            file_exists = os.path.exists(credentials_file)
            
            logger.info(f"📁 Archivo existe: {file_exists}")
            logger.info(f"📁 Ruta completa: {os.path.abspath(credentials_file)}")
            
            if not file_exists:
                return jsonify({
                    'success': False,
                    'error': f'El archivo {credentials_file} no existe',
                    'file_exists': False
                }), 500
            
            # Intentar conectar
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
            client = gspread.authorize(creds)
            
            logger.info("✅ Conectado exitosamente")
            
            # Intentar abrir la hoja
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            sheet = client.open_by_key(sheet_id)
            
            logger.info(f"✅ Hoja abierta: {sheet.title}")
            
            # Obtener la primera hoja
            worksheet = sheet.sheet1
            logger.info(f"✅ Primera hoja: {worksheet.title}")
            
            # Contar filas
            all_values = worksheet.get_all_values()
            total_rows = len(all_values)
            
            logger.info(f"📊 Total de filas: {total_rows}")
            
            if total_rows > 0:
                headers = all_values[0]
                data_rows = all_values[1:] if total_rows > 1 else []
                
                # Contar filas con datos
                non_empty_rows = [row for row in data_rows if any(cell.strip() for cell in row)]
                
                logger.info(f"📊 Filas con datos: {len(non_empty_rows)}")
                logger.info(f"📊 Headers: {len(headers)} columnas")
                
                return jsonify({
                    'success': True,
                    'sheet_title': sheet.title,
                    'worksheet_title': worksheet.title,
                    'total_rows': total_rows,
                    'data_rows': len(non_empty_rows),
                    'headers_count': len(headers),
                    'message': f'Conexión exitosa: {len(non_empty_rows)} registros encontrados'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'La hoja está vacía',
                    'total_rows': 0
                }), 500
                
        except Exception as e:
            logger.error(f"❌ Error en prueba simple: {str(e)}")
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500 