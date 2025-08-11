"""
Aplicación principal Flask - Versión Modular
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import logging

# Importar módulos propios
from config.development import DevelopmentConfig
from services.data_service import DataService
from services.google_sheets_service import GoogleSheetsConnector
from services.chart_service import ChartGenerator
from services.railway_geoserver_service import RailwayGeoServerService
from services.supabase_service import SupabaseService

# Configurar logging
import os
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
    # Configurar la aplicación
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
    data_service = DataService()
    sheets_connector = GoogleSheetsConnector()
    chart_generator = ChartGenerator()
    # Inicializar servicio GeoServer
    geoserver_service = RailwayGeoServerService()
    # Inicializar servicio Supabase
    supabase_service = SupabaseService()
    
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
    
    @app.route('/test')
    def test():
        """Ruta de prueba"""
        return "Ruta de prueba funcionando correctamente"
    
    @app.route('/datos')
    def datos():
        """Ruta para datos detallados"""
        try:
            logger.info("Accediendo a página de datos detallados")
            return render_template('pages/datos.html')
        except Exception as e:
            logger.error(f"Error en ruta de datos: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
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

    @app.route('/download/secretaria-gobierno-pdf')
    def download_secretaria_gobierno_pdf():
        """Ruta para descargar el PDF de la Secretaría Distrital de Gobierno"""
        try:
            import os
            from flask import send_file, abort
            
            # Usar ruta relativa más simple
            pdf_path = 'static/docs/Infografiia con los ojos en los residuos.pdf'
            
            # Verificar si existe el archivo
            if os.path.exists(pdf_path):
                logger.info(f"Archivo PDF encontrado en: {pdf_path}")
                logger.info(f"Tamaño del archivo: {os.path.getsize(pdf_path)} bytes")
                
                return send_file(
                    pdf_path,
                    as_attachment=True,
                    download_name='Infografia_con_los_ojos_en_los_residuos.pdf',
                    mimetype='application/pdf'
                )
            else:
                # Listar archivos en el directorio para debug
                docs_dir = 'static/docs'
                if os.path.exists(docs_dir):
                    files = os.listdir(docs_dir)
                    logger.error(f"Archivos en {docs_dir}: {files}")
                else:
                    logger.error(f"Directorio {docs_dir} no existe")
                
                logger.error(f"Archivo PDF no encontrado en: {pdf_path}")
                abort(404, description="Archivo PDF no encontrado")
                
        except Exception as e:
            logger.error(f"Error al descargar PDF: {str(e)}")
            logger.error(f"Tipo de error: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            abort(500, description=f"Error interno del servidor: {str(e)}")

    @app.route('/formulario')
    def formulario_georeferenciado():
        """Página del formulario georeferenciado"""
        return render_template('pages/formulario_georeferenciado.html')

    @app.route('/api/reportes', methods=['POST'])
    def crear_reporte():
        """Crear nuevo reporte en Supabase"""
        try:
            data = request.json
            
            # Validar datos requeridos
            required_fields = ['nombre', 'email', 'direccion', 'latitud', 'longitud', 'tipoReporte', 'descripcion']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'error': f'Campo requerido: {field}'
                    }), 400
            
            # Crear reporte
            result = supabase_service.create_report(data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Reporte creado exitosamente',
                    'report_id': result['id']
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result['error']
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/reportes', methods=['GET'])
    def obtener_reportes():
        """Obtener reportes con filtros"""
        try:
            filters = {}
            
            # Parámetros de filtro
            if request.args.get('tipo_reporte'):
                filters['tipo_reporte'] = request.args.get('tipo_reporte')
            if request.args.get('prioridad'):
                filters['prioridad'] = request.args.get('prioridad')
            if request.args.get('estado'):
                filters['estado'] = request.args.get('estado')
            if request.args.get('fecha_inicio'):
                filters['fecha_inicio'] = request.args.get('fecha_inicio')
            if request.args.get('fecha_fin'):
                filters['fecha_fin'] = request.args.get('fecha_fin')
            
            reports = supabase_service.get_reports(filters)
            
            return jsonify({
                'success': True,
                'reports': reports,
                'total': len(reports)
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/reportes/<int:report_id>/status', methods=['PUT'])
    def actualizar_estado_reporte(report_id):
        """Actualizar estado de un reporte"""
        try:
            data = request.json
            new_status = data.get('estado')
            
            if not new_status:
                return jsonify({
                    'success': False,
                    'error': 'Estado requerido'
                }), 400
            
            success = supabase_service.update_report_status(report_id, new_status)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Estado actualizado exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Error actualizando estado'
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/reportes/nearby')
    def reportes_cercanos():
        """Obtener reportes cercanos a una ubicación"""
        try:
            lat = float(request.args.get('lat', 0))
            lng = float(request.args.get('lng', 0))
            radius = float(request.args.get('radius', 5))  # km por defecto
            
            if lat == 0 and lng == 0:
                return jsonify({
                    'success': False,
                    'error': 'Coordenadas requeridas'
                }), 400
            
            reports = supabase_service.get_reports_by_location(lat, lng, radius)
            
            return jsonify({
                'success': True,
                'reports': reports,
                'total': len(reports),
                'center': {'lat': lat, 'lng': lng},
                'radius_km': radius
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/reportes/statistics')
    def estadisticas_reportes():
        """Obtener estadísticas de reportes"""
        try:
            stats = supabase_service.get_statistics()
            
            return jsonify({
                'success': True,
                'statistics': stats
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
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
    
    @app.route('/api/data')
    def get_data():
        """API para obtener datos"""
        try:
            logger.info("Solicitando datos desde API")
            
            # Obtener datos reales desde Google Sheets
            raw_data = sheets_connector.get_data()
            processed_data = data_service.process_raw_data(raw_data)
            
            # Preparar respuesta
            response = {
                'data': processed_data['data'],
                'statistics': processed_data['statistics'],
                'last_update': '2024-01-01T00:00:00',
                'columns_order': processed_data.get('columns_order', [])
            }
            
            logger.info(f"Datos obtenidos exitosamente: {len(response['data'])} registros")
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error obteniendo datos: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/refresh')
    def refresh_data():
        """API para refrescar datos"""
        try:
            logger.info("Refrescando datos")
            
            # Forzar actualización de datos
            sheets_connector.refresh_cache()
            
            return jsonify({'success': True, 'message': 'Datos actualizados correctamente'})
            
        except Exception as e:
            logger.error(f"Error refrescando datos: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/charts/participacion')
    def get_participacion_chart():
        """API para obtener gráfico de participación"""
        try:
            logger.info("Generando gráfico de participación")
            
            # Obtener datos
            raw_data = sheets_connector.get_data()
            processed_data = data_service.process_raw_data(raw_data)
            
            # Generar gráfico
            chart_data = chart_generator.generate_participacion_chart(processed_data['data'])
            
            return jsonify(chart_data)
            
        except Exception as e:
            logger.error(f"Error generando gráfico de participación: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/charts/diario')
    def get_diario_chart():
        """API para obtener gráfico diario"""
        try:
            logger.info("Generando gráfico diario")
            
            # Obtener datos
            raw_data = sheets_connector.get_data()
            processed_data = data_service.process_raw_data(raw_data)
            
            # Generar gráfico
            chart_data = chart_generator.generate_diario_chart(processed_data['data'])
            
            return jsonify(chart_data)
            
        except Exception as e:
            logger.error(f"Error generando gráfico diario: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/el-consuelo/data')
    def api_el_consuelo_data():
        """API para obtener datos de encuestas de El Consuelo"""
        try:
            # Obtener datos reales desde Google Sheets de El Consuelo
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            credentials_file = 'credentials/credentials_consuelo.json'
            consuelo_connector = GoogleSheetsConnector(credentials_file=credentials_file)
            raw_data = consuelo_connector.get_data(sheet_id)
            
            return jsonify({'data': raw_data, 'total': len(raw_data)})
        except Exception as e:
            return jsonify({'error': str(e), 'data': []}), 500
    
    @app.route('/api/geoserver/layers')
    def get_geoserver_layers():
        """Obtener capas disponibles en GeoServer"""
        try:
            layers = geoserver_service.list_layers()
            return jsonify({
                'success': True,
                'layers': layers
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/api/geoserver/upload-layer', methods=['POST'])
    def upload_layer_to_geoserver():
        """Subir nueva capa a GeoServer"""
        try:
            file = request.files['shapefile']
            layer_name = request.form['layer_name']
            workspace = request.form['workspace']
            
            # Guardar archivo temporalmente
            temp_path = f"/tmp/{layer_name}.zip"
            file.save(temp_path)
            
            # Subir a GeoServer
            if geoserver_service.upload_shapefile(temp_path, workspace, layer_name):
                return jsonify({
                    'success': True,
                    'message': f'Capa {layer_name} creada exitosamente'
                })
            
            return jsonify({
                'success': False,
                'error': 'Error al crear la capa'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/api/geoserver/create-geojson-layer', methods=['POST'])
    def create_geojson_layer():
        """Crear capa desde GeoJSON"""
        try:
            data = request.json
            workspace = data.get('workspace')
            layer_name = data.get('layer_name')
            geojson_data = data.get('geojson')
            
            if geoserver_service.create_layer_from_geojson(workspace, layer_name, geojson_data):
                return jsonify({
                    'success': True,
                    'message': f'Capa GeoJSON {layer_name} creada exitosamente'
                })
            
            return jsonify({
                'success': False,
                'error': 'Error al crear la capa GeoJSON'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/api/geoserver/wms-url/<workspace>/<layer>')
    def get_wms_url(workspace, layer):
        """Obtener URL de capa WMS"""
        try:
            wms_url = geoserver_service.get_wms_layer_url(workspace, layer)
            return jsonify({
                'success': True,
                'wms_url': wms_url
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/api/geoserver/wfs-features/<workspace>/<layer>')
    def get_wfs_features(workspace, layer):
        """Obtener features WFS"""
        try:
            filter_param = request.args.get('filter')
            features = geoserver_service.get_wfs_features(workspace, layer, filter_param)
            return jsonify({
                'success': True,
                'features': features
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/api/geoserver/update-from-sheets', methods=['POST'])
    def update_geoserver_from_sheets():
        """Actualizar capa en GeoServer con datos de Google Sheets"""
        try:
            # Obtener datos de Google Sheets
            sheets_connector = GoogleSheetsConnector()
            data = sheets_connector.get_data()
            
            # Convertir a GeoJSON
            geojson_features = []
            for row in data:
                if 'latitud' in row and 'longitud' in row:
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(row['longitud']), float(row['latitud'])]
                        },
                        "properties": {
                            "id": row.get('id', ''),
                            "barrio": row.get('barrio', ''),
                            "upz": row.get('upz', ''),
                            "estado": row.get('estado', ''),
                            "fecha": row.get('fecha', '')
                        }
                    }
                    geojson_features.append(feature)
            
            geojson_data = {
                "type": "FeatureCollection",
                "features": geojson_features
            }
            
            # Actualizar capa en GeoServer
            workspace = "santafe"
            layer_name = "puntos_criticos"
            
            if geoserver_service.create_layer_from_geojson(workspace, layer_name, geojson_data):
                return jsonify({
                    'success': True,
                    'message': 'Capa actualizada exitosamente desde Google Sheets',
                    'features_count': len(geojson_features)
                })
            
            return jsonify({
                'success': False,
                'error': 'Error al actualizar la capa'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
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
    import os
    from config.production import ProductionConfig
    from config.development import DevelopmentConfig
    
    # Determinar configuración basada en variable de entorno
    if os.environ.get('FLASK_ENV') == 'production':
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig
    
    app = create_app(config_class)
    
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 