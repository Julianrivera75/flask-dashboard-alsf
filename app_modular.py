"""
Aplicación principal Flask - Versión Modular
"""

from flask import Flask, render_template, jsonify, request
import os
import logging
from datetime import datetime

# Importar módulos propios
from config.development import DevelopmentConfig
from services.data_service import DataService
from services.google_sheets_service import GoogleSheetsConnector
from services.chart_service import ChartGenerator

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
    
    @app.route('/')
    def index():
        """Ruta principal - Home"""
        try:
            logger.info("Accediendo a la página principal")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error en ruta principal: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/san-bernardo')
    def san_bernardo():
        """Ruta para el dashboard del Barrio San Bernardo"""
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
            raw_data = sheets_connector.get_data(sheet_id)
            num_encuestas = len(raw_data)
            # Extraer datos para las gráficas de torta
            sexo_counts = {}
            nivel_educativo_counts = {}
            tiempo_reside_counts = {}
            tiempo_counts = {}  # Inicializar tiempo_counts aquí
            for row in raw_data:
                sexo = row.get('Sexo', '').strip()
                nivel = row.get('Nivel educativo', '').strip()
                tiempo = row.get('¿Hace cuanto tiempo reside en el barrio?', '').strip()
                if sexo:
                    sexo_counts[sexo] = sexo_counts.get(sexo, 0) + 1
                if nivel:
                    nivel_educativo_counts[nivel] = nivel_educativo_counts.get(nivel, 0) + 1
                if tiempo:
                    tiempo_reside_counts[tiempo] = tiempo_reside_counts.get(tiempo, 0) + 1
            # Procesar columna O (limpieza general) para gráfica de torta
            limpieza_col = 'Como calificaria la limpieza general del barrio'
            limpieza_counts = {}
            # Procesar solo filas O2 a O440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila O2) hasta 442 (incluye 441)
                valor = row.get(limpieza_col, '').strip()
                if valor in ['1', '2', '3', '4', '5']:
                    limpieza_counts[valor] = limpieza_counts.get(valor, 0) + 1
                elif valor:
                    limpieza_counts['No responde'] = limpieza_counts.get('No responde', 0) + 1

            # Si limpieza_counts está vacío, mostrar mensaje de depuración
            if not limpieza_counts:
                print('ADVERTENCIA: No se encontraron datos en la columna de limpieza')
                print('Nombre de columna buscado:', limpieza_col)
                print('Headers disponibles:', list(raw_data[0].keys()) if raw_data else 'No hay datos')

            # Depuración: imprimir datos de limpieza
            print("Limpieza counts:", limpieza_counts)
            print("Limpieza counts keys:", list(limpieza_counts.keys()))
            print("Limpieza counts values:", list(limpieza_counts.values()))
            print("Total de filas procesadas (O2-O440):", len(raw_data[0:442]))
            print("Total de registros en raw_data:", len(raw_data))
            print("Rango procesado: desde índice 0 hasta", len(raw_data[0:442]), "CORREGIDO - 439 REGISTROS - FORZADO")
            
            # Procesar columna P (frecuencia residuos) para gráfica de barras
            residuos_col = '¿Con qué frecuencia observa residuos en las calles o zonas comunes?'
            residuos_counts = {}
            # Procesar solo filas P2 a P440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila P2) hasta 442 (incluye 441)
                valor = row.get(residuos_col, '').strip()
                if valor:
                    residuos_counts[valor] = residuos_counts.get(valor, 0) + 1
            
            print(f"Residuos counts: {residuos_counts}")
            print(f"Residuos counts keys: {list(residuos_counts.keys())}")
            print(f"Residuos counts values: {list(residuos_counts.values())}")
            print(f"Total de filas procesadas para residuos: {len(raw_data[0:442])}")
            
            # Procesar columna Q (afecta imagen del barrio) para gráfica de barras
            imagen_col = '¿Considera que la acumulación de residuos afecta la imagen del barrio?'
            # Procesar columna Q (afecta imagen del barrio) para gráfica de barras
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila Q2) hasta 442 (incluye 441)
                valor = row.get(imagen_col, '').strip()
                if valor:
                    tiempo_counts[valor] = tiempo_counts.get(valor, 0) + 1
            
            print(f"Imagen counts: {tiempo_counts}")
            print(f"Imagen counts keys: {list(tiempo_counts.keys())}")
            print(f"Imagen counts values: {list(tiempo_counts.values())}")
            print(f"Total de filas procesadas para imagen: {len(raw_data[0:442])}")
            
            # Procesar columna R (residuos y seguridad) para gráfica de barras
            seguridad_col = '¿Considera que el tema de residuos esta relacionado con el tema de seguridad del barrio?'
            seguridad_counts = {}
            # Procesar columna R (residuos y seguridad) para gráfica de barras
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila R2) hasta 442 (incluye 441)
                valor = row.get(seguridad_col, '').strip()
                if valor:
                    seguridad_counts[valor] = seguridad_counts.get(valor, 0) + 1
            
            print(f"Seguridad counts: {seguridad_counts}")
            print(f"Seguridad counts keys: {list(seguridad_counts.keys())}")
            print(f"Seguridad counts values: {list(seguridad_counts.values())}")
            print(f"Total de filas procesadas para seguridad: {len(raw_data[0:442])}")
            
            # Procesar columna S (afecta calidad de vida) para gráfica de barras
            calidad_vida_col = '¿Considera que la acumulación de residuos afecta su calidad de vida?'
            calidad_vida_counts = {}
            # Procesar solo filas S2 a S440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila S2) hasta 442 (incluye 441)
                valor = row.get(calidad_vida_col, '').strip()
                if valor:
                    calidad_vida_counts[valor] = calidad_vida_counts.get(valor, 0) + 1
            
            print(f"Calidad de vida counts: {calidad_vida_counts}")
            print(f"Calidad de vida counts keys: {list(calidad_vida_counts.keys())}")
            print(f"Calidad de vida counts values: {list(calidad_vida_counts.values())}")
            print(f"Total de filas procesadas para calidad de vida: {len(raw_data[0:442])}")
            
            # Procesar columna T (separación de residuos) para gráfica de barras
            separacion_col = '¿Separa los residuos en su casa (orgánicos, reciclables, no reciclables)?'
            separacion_counts = {}
            # Procesar solo filas T2 a T440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila T2) hasta 442 (incluye 441)
                valor = row.get(separacion_col, '').strip()
                if valor:
                    separacion_counts[valor] = separacion_counts.get(valor, 0) + 1
            
            print(f"Separación counts: {separacion_counts}")
            print(f"Separación counts keys: {list(separacion_counts.keys())}")
            print(f"Separación counts values: {list(separacion_counts.values())}")
            print(f"Total de filas procesadas para separación: {len(raw_data[0:442])}")
            
            # Procesar columna U (conoce horario recolección) para gráfica de barras
            horario_col = '¿Conoce el horario de recolección de residuos en el barrio?'
            horario_counts = {}
            # Procesar solo filas U2 a U440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila U2) hasta 442 (incluye 441)
                valor = row.get(horario_col, '').strip()
                if valor:
                    horario_counts[valor] = horario_counts.get(valor, 0) + 1
            
            print(f"Horario counts: {horario_counts}")
            print(f"Horario counts keys: {list(horario_counts.keys())}")
            print(f"Horario counts values: {list(horario_counts.values())}")
            print(f"Total de filas procesadas para horario: {len(raw_data[0:442])}")
            
            # Procesar columna V (saca residuos en horarios) para gráfica de barras
            saca_horarios_col = '¿Saca los residuos en los horarios establecidos?'
            saca_horarios_counts = {}
            # Procesar solo filas V2 a V440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila V2) hasta 442 (incluye 441)
                valor = row.get(saca_horarios_col, '').strip()
                if valor:
                    saca_horarios_counts[valor] = saca_horarios_counts.get(valor, 0) + 1
            
            print(f"Saca horarios counts: {saca_horarios_counts}")
            print(f"Saca horarios counts keys: {list(saca_horarios_counts.keys())}")
            print(f"Saca horarios counts values: {list(saca_horarios_counts.values())}")
            print(f"Total de filas procesadas para saca horarios: {len(raw_data[0:442])}")
            
            # Procesar columna W (entrega a recuperador) para gráfica de barras
            recuperador_col = '¿Entrega sus residuos aprovechables a un recuperador de oficio?'
            recuperador_counts = {}
            # Procesar solo filas W2 a W440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila W2) hasta 442 (incluye 441)
                valor = row.get(recuperador_col, '').strip()
                if valor:
                    recuperador_counts[valor] = recuperador_counts.get(valor, 0) + 1
            
            print(f"Recuperador counts: {recuperador_counts}")
            print(f"Recuperador counts keys: {list(recuperador_counts.keys())}")
            print(f"Recuperador counts values: {list(recuperador_counts.values())}")
            print(f"Total de filas procesadas para recuperador: {len(raw_data[0:442])}")
            
            # Procesar columna X (lugar disposición) para gráfica de barras
            lugar_col = '¿En que lugar dispone los residuos?'
            lugar_counts = {}
            # Procesar solo filas X2 a X440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila X2) hasta 442 (incluye 441)
                valor = row.get(lugar_col, '').strip()
                if valor:
                    lugar_counts[valor] = lugar_counts.get(valor, 0) + 1
            
            print(f"Lugar counts: {lugar_counts}")
            print(f"Lugar counts keys: {list(lugar_counts.keys())}")
            print(f"Lugar counts values: {list(lugar_counts.values())}")
            print(f"Total de filas procesadas para lugar: {len(raw_data[0:442])}")
            
            # Procesar columna Z (calificación servicio) para gráfica de barras
            servicio_col = '¿Cómo calificaría la operación del servicio de aseo de Promoambiental Distrito S.A.S?'
            servicio_counts = {}
            # Procesar solo filas Z2 a Z440 (registros 1 a 439 en raw_data)
            for i, row in enumerate(raw_data[0:442], start=2):  # Empezar desde índice 0 (fila Z2) hasta 442 (incluye 441)
                valor = row.get(servicio_col, '').strip()
                if valor:
                    servicio_counts[valor] = servicio_counts.get(valor, 0) + 1
            
            print(f"Servicio counts: {servicio_counts}")
            print(f"Servicio counts keys: {list(servicio_counts.keys())}")
            print(f"Servicio counts values: {list(servicio_counts.values())}")
            print(f"Total de filas procesadas para servicio: {len(raw_data[0:442])}")
            
            # Procesar columna AA (frecuencia camión) para gráfica de barras
            frecuencia_camion_col = '¿Con qué frecuencia pasa el camión recolector de residuos?'
            frecuencia_camion_counts = {}
            for row in raw_data[0:442]:
                if frecuencia_camion_col in row:
                    valor = row[frecuencia_camion_col].strip() if row[frecuencia_camion_col] else 'No responde'
                    frecuencia_camion_counts[valor] = frecuencia_camion_counts.get(valor, 0) + 1
            
            print(f"Frecuencia camión counts: {frecuencia_camion_counts}")
            print(f"Frecuencia camión counts keys: {list(frecuencia_camion_counts.keys())}")
            print(f"Frecuencia camión counts values: {list(frecuencia_camion_counts.values())}")
            print(f"Total de filas procesadas para frecuencia camión: {len(raw_data[0:442])}")
            
            # Procesar columna AB (participación campañas) para gráfica de barras
            participacion_col = '¿Ha participado en alguna campaña de limpieza o educación ambiental en su barrio?'
            participacion_counts = {}
            for row in raw_data[0:442]:
                if participacion_col in row:
                    valor = row[participacion_col].strip() if row[participacion_col] else 'No responde'
                    participacion_counts[valor] = participacion_counts.get(valor, 0) + 1
            
            print(f"Participación counts: {participacion_counts}")
            print(f"Participación counts keys: {list(participacion_counts.keys())}")
            print(f"Participación counts values: {list(participacion_counts.values())}")
            print(f"Total de filas procesadas para participación: {len(raw_data[0:442])}")
            
            # Procesar columna AC (iniciativas comunitarias) para gráfica de barras
            iniciativas_col = '\xa0¿Le gustaría participar en iniciativas comunitarias de limpieza?'
            iniciativas_counts = {}
            for row in raw_data[0:442]:
                if iniciativas_col in row:
                    valor = row[iniciativas_col].strip() if row[iniciativas_col] else 'No responde'
                    iniciativas_counts[valor] = iniciativas_counts.get(valor, 0) + 1
            
            print(f"Iniciativas counts: {iniciativas_counts}")
            print(f"Iniciativas counts keys: {list(iniciativas_counts.keys())}")
            print(f"Iniciativas counts values: {list(iniciativas_counts.values())}")
            print(f"Total de filas procesadas para iniciativas: {len(raw_data[0:442])}")
            
            # Procesar columna AD (educación ambiental) para gráfica de barras
            educacion_col = '¿Considera que hace falta más educación ambiental en el barrio?'
            educacion_counts = {}
            for row in raw_data[0:442]:
                if educacion_col in row:
                    valor = row[educacion_col].strip() if row[educacion_col] else 'No responde'
                    educacion_counts[valor] = educacion_counts.get(valor, 0) + 1
            
            print(f"Educación counts: {educacion_counts}")
            print(f"Educación counts keys: {list(educacion_counts.keys())}")
            print(f"Educación counts values: {list(educacion_counts.values())}")
            print(f"Total de filas procesadas para educación: {len(raw_data[0:442])}")
            
            # Procesar columna AE (sabe punto crítico) para gráfica de barras
            punto_critico_col = '¿Sabe que es un punto critico?'
            punto_critico_counts = {}
            for row in raw_data[0:442]:
                if punto_critico_col in row:
                    valor = row[punto_critico_col].strip() if row[punto_critico_col] else 'No responde'
                    punto_critico_counts[valor] = punto_critico_counts.get(valor, 0) + 1
            
            print(f"Punto crítico counts: {punto_critico_counts}")
            print(f"Punto crítico counts keys: {list(punto_critico_counts.keys())}")
            print(f"Punto crítico counts values: {list(punto_critico_counts.values())}")
            print(f"Total de filas procesadas para punto crítico: {len(raw_data[0:442])}")
            
            # Procesar columna AF (identifica puntos críticos) para gráfica de barras
            identifica_col = '¿Identifica puntos críticos en el barrio?'
            identifica_counts = {}
            for row in raw_data[0:442]:
                if identifica_col in row:
                    valor = row[identifica_col].strip() if row[identifica_col] else 'No responde'
                    identifica_counts[valor] = identifica_counts.get(valor, 0) + 1
            
            print(f"Identifica counts: {identifica_counts}")
            print(f"Identifica counts keys: {list(identifica_counts.keys())}")
            print(f"Identifica counts values: {list(identifica_counts.values())}")
            print(f"Total de filas procesadas para identifica: {len(raw_data[0:442])}")
            
            # Procesar columna AG (tiempo puntos críticos) para gráfica de barras
            tiempo_puntos_col = '¿Cada cuanto tiempo ve estos puntos en el barrio?'
            tiempo_puntos_counts = {}
            for row in raw_data[0:442]:
                if tiempo_puntos_col in row:
                    valor = row[tiempo_puntos_col].strip() if row[tiempo_puntos_col] else 'No responde'
                    tiempo_puntos_counts[valor] = tiempo_puntos_counts.get(valor, 0) + 1
            
            print(f"Tiempo puntos counts: {tiempo_puntos_counts}")
            print(f"Tiempo puntos counts keys: {list(tiempo_puntos_counts.keys())}")
            print(f"Tiempo puntos counts values: {list(tiempo_puntos_counts.values())}")
            print(f"Total de filas procesadas para tiempo puntos: {len(raw_data[0:442])}")
            
            # Procesar columna AH (horario saca residuos) para gráfica de barras

            
            # Debug: mostrar primeros valores de columna P
            if raw_data and len(raw_data) > 1:
                headers = list(raw_data[0].keys()) if raw_data else []
                col_p = headers[15] if len(headers) > 15 else None
                print(f'Columna P (índice 15): {repr(col_p)}')
                print('Primeros 10 valores de columna P:')
                for row in raw_data[1:11]:  # Filas 2 a 11
                    print(row.get(col_p, '') if col_p else 'Columna no encontrada')

            print("Entrando a la ruta /el-consuelo y ejecutando depuración de headers...")
            # Depuración: imprimir headers y primeros valores de la columna O
            if raw_data:
                headers = list(raw_data[0].keys())
                print('Headers:')
                for idx, h in enumerate(headers):
                    print(f'{idx}: {repr(h)}')
                if len(headers) > 14:
                    col_o = headers[14]
                    print(f'Columna O (índice 14): {repr(col_o)}')
                    print('Primeros 10 valores de columna O:')
                    for row in raw_data[:10]:
                        print(row.get(col_o, ''))

            return render_template(
                'pages/el_consuelo.html',
                num_encuestas=num_encuestas,
                sexo_counts=sexo_counts,
                nivel_educativo_counts=nivel_educativo_counts,
                tiempo_reside_counts=tiempo_reside_counts,
                limpieza_counts=limpieza_counts,
                residuos_counts=residuos_counts,
                tiempo_counts=tiempo_counts,
                seguridad_counts=seguridad_counts,
                calidad_vida_counts=calidad_vida_counts,
                separacion_counts=separacion_counts,
                horario_counts=horario_counts,
                saca_horarios_counts=saca_horarios_counts,
                recuperador_counts=recuperador_counts,
                lugar_counts=lugar_counts,
                servicio_counts=servicio_counts,
                frecuencia_camion_counts=frecuencia_camion_counts,
                participacion_counts=participacion_counts,
                iniciativas_counts=iniciativas_counts,
                educacion_counts=educacion_counts,
                punto_critico_counts=punto_critico_counts,
                identifica_counts=identifica_counts,
                tiempo_puntos_counts=tiempo_puntos_counts,
                consuelo_data=raw_data
            )
        except Exception as e:
            logger.error(f"Error en dashboard de El Consuelo: {str(e)}")
            return render_template('error.html', error=str(e)), 500
    
    @app.route('/api/data')
    def get_data():
        """API para obtener datos"""
        try:
            logger.info("Solicitando datos desde API")
            
            # Obtener datos de Google Sheets
            raw_data = sheets_connector.get_data()
            
            # Depuración: imprimir headers y primeros valores de la columna O
            if raw_data:
                headers = list(raw_data[0].keys())
                print('Headers:')
                for idx, h in enumerate(headers):
                    print(f'{idx}: {repr(h)}')
                if len(headers) > 14:
                    col_o = headers[14]
                    print(f'Columna O (índice 14): {repr(col_o)}')
                    print('Primeros 10 valores de columna O:')
                    for row in raw_data[:10]:
                        print(row.get(col_o, ''))
            
            # Procesar datos usando el servicio
            processed_data = data_service.process_raw_data(raw_data)
            
            # Preparar respuesta
            response = {
                'data': [record['original'] for record in processed_data['data']],
                'statistics': processed_data['statistics'],
                'validation': processed_data['validation'],
                'last_update': datetime.now().isoformat(),
                'columns_order': list(processed_data['data'][0]['original'].keys()) if processed_data['data'] else []
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
            sheet_id = '1265C_6-JZ-ZzeUD4RRZ1cKoVYOVvysztvWLx63dh2TM'
            credentials_file = 'credentials/credentials_consuelo.json'
            sheets_connector = GoogleSheetsConnector(credentials_file=credentials_file, credentials_env_var="GOOGLE_CREDENTIALS_CONSUELO_JSON")
            raw_data = sheets_connector.get_data(sheet_id)
            return jsonify({'data': raw_data, 'total': len(raw_data)})
        except Exception as e:
            return jsonify({'error': str(e), 'data': []}), 500
    
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