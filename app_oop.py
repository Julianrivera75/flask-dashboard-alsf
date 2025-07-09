from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import zipfile
import xml.etree.ElementTree as ET
import folium

from data_manager import DataManager
from google_sheets_connector import GoogleSheetsConnector
from chart_generator import ChartGenerator
from config import Config

# Cargar variables de entorno
load_dotenv('credentials/config.env')

class BogotaApp:
    """
    Clase principal de la aplicación Flask para Alcaldía Local de Santa Fe
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        self.data_manager = DataManager()
        self.sheets_connector = GoogleSheetsConnector()
        self.chart_generator = ChartGenerator(self.data_manager)
        self.scheduler = BackgroundScheduler()
        self.sheet_id = Config.GOOGLE_SHEET_ID
        
        self.setup_routes()
        self.setup_scheduler()
    
    def setup_routes(self):
        """Configurar todas las rutas de la aplicación"""
        
        @self.app.route('/')
        def index():
            """Página principal"""
            return render_template('index.html')
        
        @self.app.route('/api/data')
        def get_data():
            """API para obtener datos"""
            data, columns_order, last_update = self.data_manager.get_data()
            
            if data is None:
                return jsonify({'error': 'No hay datos disponibles'}), 404
            
            return jsonify({
                'data': data,
                'columns_order': columns_order,
                'last_update': last_update.isoformat() if last_update else None
            })
        
        @self.app.route('/api/refresh')
        def refresh_data():
            """API para refrescar datos manualmente"""
            try:
                # Obtener datos de Google Sheets
                data, columns_order = self.sheets_connector.get_sheet_data(self.sheet_id)
                
                if data is None:
                    return jsonify({'error': 'No se pudieron obtener datos de Google Sheets'}), 500
                
                # Actualizar datos
                data_changed = self.data_manager.update_data(data, columns_order)
                
                return jsonify({
                    'success': True,
                    'data_changed': data_changed,
                    'record_count': len(data),
                    'last_update': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': f'Error refrescando datos: {str(e)}'}), 500
        
        @self.app.route('/api/indicators')
        def get_indicators():
            """API para obtener indicadores"""
            indicators = self.data_manager.get_indicators()
            return jsonify(indicators)
        
        @self.app.route('/api/reset-homicide', methods=['POST'])
        def reset_homicide():
            """API para resetear contador de homicidios"""
            data = request.get_json()
            code = data.get('code', '')
            
            if self.data_manager.reset_homicide_counter(code):
                return jsonify({'success': True, 'message': 'Contador reseteado exitosamente'})
            else:
                return jsonify({'success': False, 'message': 'Código incorrecto'}), 400
        
        @self.app.route('/api/pie-chart')
        def get_pie_chart():
            """API para obtener gráfico de Torta"""
            chart_data = self.chart_generator.create_pie_chart()
            return jsonify(chart_data)
        
        @self.app.route('/api/daily-chart')
        def get_daily_chart():
            """API para obtener gráfico diario"""
            chart_data = self.chart_generator.create_daily_chart()
            return jsonify(chart_data)
        
        @self.app.route('/api/entity-data/<entity>')
        def get_entity_data(entity):
            """API para obtener datos de una entidad específica"""
            chart_data = self.chart_generator.create_monthly_chart(entity)
            summary_data = self.chart_generator.get_entity_summary(entity)
            
            return jsonify({
                'chart_data': chart_data,
                'summary_data': summary_data
            })
    
    def setup_scheduler(self):
        """Configurar el programador de tareas"""
        def fetch_data_job():
            """Tarea programada para obtener datos"""
            try:
                data, columns_order = self.sheets_connector.get_sheet_data(self.sheet_id)
                if data is not None:
                    self.data_manager.update_data(data, columns_order)
            except Exception as e:
                print(f"Error en tarea programada: {e}")
        
        # Programar actualización cada hora
        self.scheduler.add_job(
            func=fetch_data_job,
            trigger="interval",
            hours=Config.REFRESH_INTERVAL_HOURS,
            id="fetch_data_from_sheets"
        )
        
        # Ejecutar una vez al inicio
        fetch_data_job()
        
        # Iniciar el programador
        self.scheduler.start()
    
    def run(self, debug=None, host=None, port=None):
        """Ejecutar la aplicación"""
        debug = debug if debug is not None else Config.DEBUG
        host = host or Config.HOST
        port = port or Config.PORT
        
        try:
            print(f"🚀 Iniciando {Config.APP_NAME}")
            print(f"📍 Servidor: http://{host}:{port}")
            print(f"🔧 Modo debug: {debug}")
            self.app.run(debug=debug, host=host, port=port)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo la aplicación...")
        finally:
            if self.scheduler.running:
                self.scheduler.shutdown()

# Función para crear la instancia de la aplicación
def create_app():
    """Factory function para crear la aplicación"""
    return BogotaApp()

if __name__ == '__main__':
    app = BogotaApp()
    app.run() 