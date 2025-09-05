"""
Aplicación principal Flask - Versión Modular

Copyright (c) 2024 Alcaldía Local Santa Fe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
import os
import logging
from datetime import datetime
import pytz
from flask_wtf.csrf import CSRFProtect

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
    
    # Configuración de zona horaria de Colombia
    app.config['TIMEZONE'] = 'America/Bogota'
    colombia_tz = pytz.timezone('America/Bogota')
    
    # Inicializar CSRF protection
    csrf = CSRFProtect(app)
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Configuración para producción
    if app.config.get('ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    # Inicialización automática de base de datos para Railway
    with app.app_context():
        try:
            from init_reportes_railway import init_reportes_database
            logger.info("🚀 Inicializando base de datos de reportes en Railway...")
            if init_reportes_database():
                logger.info("✅ Base de datos de reportes de Railway inicializada correctamente")
            else:
                logger.warning("⚠️  La inicialización de reportes de Railway falló, usando configuración por defecto")
        except ImportError:
            logger.info("ℹ️  Script de Railway no disponible, usando configuración por defecto")
        except Exception as e:
            logger.error(f"❌ Error en inicialización de Railway: {e}")
        
        # Crear tablas por defecto
        db.create_all()
        
        # Inicializar datos básicos de reportes si es necesario (para Railway)
        # Comentado temporalmente para evitar bucle infinito
        # try:
        #     from scripts.init_reportes_database import init_reportes_database
        #     logger.info("📊 Verificando datos básicos de reportes...")
        #     if init_reportes_database():
        #         logger.info("✅ Datos básicos de reportes verificados/cargados correctamente")
        #     else:
        #         logger.warning("⚠️  Error cargando datos básicos de reportes")
        # except ImportError:
        #     logger.info("ℹ️  Script de datos básicos de reportes no disponible")
        # except Exception as e:
        #     logger.error(f"❌ Error cargando datos básicos de reportes: {e}")
        logger.info("ℹ️  Inicialización de datos básicos deshabilitada temporalmente")
    
    # Inicializar servicios
    sheets_connector = GoogleSheetsConnector()
    
    # Registrar blueprints
    from routes.reportes import reportes_bp
    from routes.analytics_routes import analytics_bp
    from routes.acciones_1000_routes import acciones_1000_bp
    from routes.buscar_reportes import buscar_reportes_bp
    app.register_blueprint(reportes_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(acciones_1000_bp)
    app.register_blueprint(buscar_reportes_bp)
    
    # Ruta de prueba temporal
    @app.route('/test-app')
    def test_app():
        return jsonify({'success': True, 'message': 'App funcionando'})
    
    # Inicializar middleware de analytics
    from middleware.analytics_middleware import init_analytics_middleware
    init_analytics_middleware(app)
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Servir archivos subidos (fotos de actividades)"""
        try:
            # Construir la ruta completa del archivo
            # Las fotos se guardan en static/uploads/acciones_1000/
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            file_path = os.path.join(upload_folder, filename)
            
            # Crear directorio de uploads si no existe
            os.makedirs(upload_folder, exist_ok=True)
            
            # Verificar que el archivo existe y está dentro del directorio de uploads
            if os.path.exists(file_path) and os.path.commonpath([upload_folder, file_path]) == upload_folder:
                return send_file(file_path)
            else:
                logger.warning(f"Archivo no encontrado: {file_path}")
                return "Archivo no encontrado", 404
        except Exception as e:
            logger.error(f"Error al servir archivo {filename}: {e}")
            return "Error interno del servidor", 500
    
    @app.route('/')
    def index():
        """Ruta principal - Home"""
        try:
            logger.info("Accediendo a la página principal")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error en ruta principal: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    def init_database():
        """Función para inicializar la base de datos de manera inteligente"""
        try:
            with app.app_context():
                # Crear todas las tablas
                db.create_all()
                
                # Importar modelos
                from models import Responsable, TipoActividad, Entidad, Sector
                
                logger.info("🔄 Inicializando base de datos de manera inteligente...")
                
                # 1. RESPONSABLES - Solo agregar los que falten
                responsables_existentes = {r.nombre.lower() for r in Responsable.query.all()}
                responsables_basicos = [
                    # Opciones básicas sin secretarías ni alcaldía local
                    # Agregar aquí solo las opciones que realmente necesites
                ]
                
                responsables_agregados = 0
                for nombre in responsables_basicos:
                    if nombre.lower() not in responsables_existentes:
                        responsable = Responsable(nombre=nombre, activo=True)
                        db.session.add(responsable)
                        responsables_agregados += 1
                        logger.info(f"➕ Agregado responsable: {nombre}")
                
                # 2. TIPOS DE ACTIVIDAD - Solo agregar los que falten
                tipos_existentes = {t.nombre.lower() for t in TipoActividad.query.all()}
                tipos_basicos = [
                    # Opciones básicas sin los tipos no deseados
                    # Agregar aquí solo los tipos que realmente necesites
                ]
                
                tipos_agregados = 0
                for nombre in tipos_basicos:
                    if nombre.lower() not in tipos_existentes:
                        tipo = TipoActividad(nombre=nombre, activo=True)
                        db.session.add(tipo)
                        tipos_agregados += 1
                        logger.info(f"➕ Agregado tipo de actividad: {nombre}")
                
                # 3. ENTIDADES - Solo agregar las que falten
                entidades_existentes = {e.nombre.lower() for e in Entidad.query.all()}
                entidades_basicas = [
                    "Alcaldía Mayor de Bogotá",
                    "Policía Nacional",
                    "Bomberos",
                    "Secretaría de Salud",
                    "Secretaría de Integración Social",
                    "OTRA"
                ]
                
                entidades_agregadas = 0
                for nombre in entidades_basicas:
                    if nombre.lower() not in entidades_existentes:
                        entidad = Entidad(nombre=nombre, activo=True)
                        db.session.add(entidad)
                        entidades_agregadas += 1
                        logger.info(f"➕ Agregada entidad: {nombre}")
                
                # 4. SECTORES - Solo agregar los que falten
                sectores_existentes = {s.nombre.lower() for s in Sector.query.all()}
                sectores_basicos = [
                    "Sector 1",
                    "Sector 2", 
                    "Sector 3"
                ]
                
                sectores_agregados = 0
                for nombre in sectores_basicos:
                    if nombre.lower() not in sectores_existentes:
                        sector = Sector(nombre=nombre, activo=True)
                        db.session.add(sector)
                        sectores_agregados += 1
                        logger.info(f"➕ Agregado sector: {nombre}")
                
                # Hacer commit solo si se agregaron nuevos datos
                if any([responsables_agregados, tipos_agregados, entidades_agregadas, sectores_agregados]):
                    try:
                        db.session.commit()
                        logger.info(f"✅ Base de datos actualizada: {responsables_agregados} responsables, {tipos_agregados} tipos, {entidades_agregadas} entidades, {sectores_agregados} sectores agregados")
                    except Exception as commit_error:
                        logger.error(f"❌ Error en commit: {commit_error}")
                        db.session.rollback()
                        # Intentar crear al menos opciones básicas
                        try:
                            if not Responsable.query.first():
                                responsable = Responsable(nombre="Responsable General", activo=True)
                                db.session.add(responsable)
                            
                            if not TipoActividad.query.first():
                                tipo = TipoActividad(nombre="Actividad General", activo=True)
                                db.session.add(tipo)
                            
                            if not Entidad.query.first():
                                entidad = Entidad(nombre="Entidad General", activo=True)
                                db.session.add(entidad)
                            
                            db.session.commit()
                            logger.info("✅ Opciones básicas creadas como fallback")
                        except Exception as fallback_error:
                            logger.error(f"❌ Error en fallback: {fallback_error}")
                else:
                    logger.info("✅ Base de datos ya está completa, no se agregaron nuevos datos")
                
                return True
                    
        except Exception as e:
            logger.error(f"❌ Error al inicializar base de datos: {str(e)}")
            if 'db' in locals() and hasattr(db, 'session'):
                db.session.rollback()
            return False

    @app.route('/init-db')
    def init_database_route():
        """Ruta para inicializar la base de datos en Railway"""
        success = init_database()
        if success:
            return jsonify({
                'success': True,
                'message': 'Base de datos inicializada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al inicializar la base de datos'
            }), 500

    @app.route('/clean-db')
    def clean_database():
        """Ruta para limpiar opciones no deseadas de la base de datos"""
        try:
            with app.app_context():
                from models import Responsable, TipoActividad, Entidad, Sector
                
                logger.info("🧹 Limpiando opciones no deseadas de la base de datos...")
                
                # Opciones a eliminar - RESPONSABLES
                responsables_a_eliminar = [
                    "Alcaldía Local Santa Fe",
                    "Secretaría de Gobierno",
                    "Secretaría de Seguridad", 
                    "Secretaría de Salud",
                    "Secretaría de Integración Social"
                ]
                
                # Opciones a eliminar - TIPOS DE ACTIVIDAD
                tipos_a_eliminar = [
                    "Operativo de Seguridad",
                    "Jornada de Salud",
                    "Actividad Social",
                    "Mantenimiento de Espacios"
                ]
                
                # Eliminar responsables no deseados
                responsables_eliminados = 0
                for nombre in responsables_a_eliminar:
                    responsable = Responsable.query.filter_by(nombre=nombre).first()
                    if responsable:
                        db.session.delete(responsable)
                        responsables_eliminados += 1
                        logger.info(f"🗑️ Eliminado responsable: {nombre}")
                
                # Eliminar tipos de actividad no deseados
                tipos_eliminados = 0
                for nombre in tipos_a_eliminar:
                    tipo = TipoActividad.query.filter_by(nombre=nombre).first()
                    if tipo:
                        db.session.delete(tipo)
                        tipos_eliminados += 1
                        logger.info(f"🗑️ Eliminado tipo de actividad: {nombre}")
                
                # Hacer commit de los cambios
                db.session.commit()
                
                total_eliminados = responsables_eliminados + tipos_eliminados
                logger.info(f"✅ Limpieza completada: {responsables_eliminados} responsables y {tipos_eliminados} tipos eliminados")
                
                return jsonify({
                    'success': True,
                    'message': f'Limpieza completada: {total_eliminados} opciones eliminadas ({responsables_eliminados} responsables, {tipos_eliminados} tipos)'
                })
                
        except Exception as e:
            logger.error(f"❌ Error al limpiar base de datos: {str(e)}")
            if 'db' in locals() and hasattr(db, 'session'):
                db.session.rollback()
            return jsonify({
                'success': False,
                'error': f'Error al limpiar base de datos: {str(e)}'
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
            # Obtener datos directamente desde Google Sheets (sin credenciales)
            sheet_id = config.Config.EL_CONSUELO_SHEET_ID
            
            # Usar requests para obtener datos CSV directamente
            import requests
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
            
            logger.info(f"Conectando directamente a Google Sheets de El Consuelo: {sheet_url}")
            
            response = requests.get(sheet_url)
            response.raise_for_status()
            
            # Procesar CSV
            import csv
            from io import StringIO
            
            csv_text = response.text
            csv_io = StringIO(csv_text)
            reader = csv.DictReader(csv_io)
            
            # Convertir a lista de diccionarios
            raw_data = []
            for row in reader:
                raw_data.append(row)
            
            logger.info(f"Datos de El Consuelo obtenidos directamente: {len(raw_data)} registros")
            
            return jsonify({'data': raw_data, 'total': len(raw_data)})
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

def get_colombia_time():
    """Obtener la hora actual de Colombia"""
    colombia_tz = pytz.timezone('America/Bogota')
    utc_now = datetime.utcnow()
    colombia_time = colombia_tz.fromutc(utc_now)
    return colombia_time

def format_colombia_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """Formatear fecha/hora en zona horaria de Colombia"""
    if dt is None:
        return None
    
    # Si la fecha ya tiene zona horaria, convertirla
    if dt.tzinfo is not None:
        colombia_tz = pytz.timezone('America/Bogota')
        colombia_time = dt.astimezone(colombia_tz)
    else:
        # Asumir que es UTC y convertir
        utc_tz = pytz.UTC
        utc_time = utc_tz.localize(dt)
        colombia_tz = pytz.timezone('America/Bogota')
        colombia_time = utc_time.astimezone(colombia_tz)
    
    return colombia_time.strftime(format_str)

if __name__ == '__main__':
    import config
    
    app = create_app(config.DevelopmentConfig)
    
    # Configuración para desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = True
    
    app.run(host='127.0.0.1', port=port, debug=debug) 