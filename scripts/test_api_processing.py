#!/usr/bin/env python3
"""
Script de prueba para verificar el procesamiento de datos de la API de San Bernardo
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheets_service import GoogleSheetsConnector
from config import Config

# Simular la función de procesamiento del app_modular.py
def process_san_bernardo_data(raw_data):
    """
    Procesa los datos de encuestas de San Bernardo para adaptarlos al formato esperado por el frontend
    """
    if not raw_data:
        return []
    
    processed_data = []
    
    for row in raw_data:
        # Crear un registro adaptado con las columnas que espera el frontend
        processed_row = {}
        
        # Mapear fecha de finalización desde "Hora de finalización"
        fecha_finalizacion = row.get('Hora de finalización', '')
        if fecha_finalizacion:
            try:
                # La fecha viene en formato como "6/17/25 17:59"
                if '/' in fecha_finalizacion and len(fecha_finalizacion.split('/')) == 3:
                    fecha_parte = fecha_finalizacion.split(' ')[0]  # Tomar solo la parte de fecha
                    partes = fecha_parte.split('/')
                    if len(partes) == 3:
                        # Convertir a formato más legible: D/M/YY
                        processed_row['Fecha final de ejecución'] = fecha_parte
                else:
                    processed_row['Fecha final de ejecución'] = fecha_finalizacion
            except:
                processed_row['Fecha final de ejecución'] = fecha_finalizacion
        else:
            processed_row['Fecha final de ejecución'] = ''
        
        # Simular población impactada (cada encuesta representa 1 persona)
        processed_row['Población impactada'] = 1
        
        # Agregar información del encuestador como "Entidad"
        encuestador = row.get('Nombre del encuestador', 'Sin especificar')
        processed_row['Entidad'] = encuestador
        
        # Agregar descripción basada en los datos de la encuesta
        barrio_tiempo = row.get('¿Hace cuanto tiempo reside en el barrio?', '')
        limpieza = row.get('Como calificaria la limpieza general del barrio', '')
        
        descripcion_parts = []
        if barrio_tiempo:
            descripcion_parts.append(f"Reside en el barrio: {barrio_tiempo}")
        if limpieza:
            descripcion_parts.append(f"Calificación limpieza: {limpieza}")
        
        processed_row['Descripción de los compromisos'] = ' | '.join(descripcion_parts) if descripcion_parts else 'Encuesta de residuos'
        
        # Agregar resumen de actividades
        puntos_criticos = row.get('¿Identifica puntos críticos en el barrio?', '')
        frecuencia_residuos = row.get('¿Con qué frecuencia observa residuos en las calles o zonas comunes?', '')
        
        resumen_parts = []
        if puntos_criticos:
            resumen_parts.append(f"Puntos críticos: {puntos_criticos}")
        if frecuencia_residuos:
            resumen_parts.append(f"Frecuencia residuos: {frecuencia_residuos}")
        
        processed_row['Resumen de actividades'] = ' | '.join(resumen_parts) if resumen_parts else 'Participación en encuesta'
        
        # Mantener datos originales para referencia
        processed_row.update(row)
        
        processed_data.append(processed_row)
    
    return processed_data

def test_data_processing():
    """Prueba el procesamiento de datos de la API"""
    print("🧪 PRUEBA DE PROCESAMIENTO DE DATOS API SAN BERNARDO")
    print("=" * 60)
    
    # Crear instancia de configuración
    config = Config()
    
    try:
        # Conectar a Google Sheets
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        if not connector.connect():
            print("❌ No se pudo conectar a Google Sheets")
            return False
        
        print("✅ Conexión exitosa con Google Sheets")
        
        # Obtener datos en bruto
        raw_data, headers = connector.get_sheet_data(config.SAN_BERNARDO_SHEET_ID)
        
        if not raw_data:
            print("❌ No se pudieron obtener datos")
            return False
        
        print(f"📊 Datos en bruto obtenidos: {len(raw_data)} registros")
        print(f"📋 Columnas disponibles: {len(headers)}")
        
        # Procesar los datos
        processed_data = process_san_bernardo_data(raw_data)
        
        print(f"📈 Datos procesados: {len(processed_data)} registros")
        
        if processed_data:
            # Mostrar ejemplo del primer registro procesado
            primer_registro = processed_data[0]
            print("\n🔍 EJEMPLO DE REGISTRO PROCESADO:")
            print("-" * 40)
            
            # Mostrar columnas clave que espera el frontend
            columnas_clave = [
                'Fecha final de ejecución',
                'Población impactada', 
                'Entidad',
                'Descripción de los compromisos',
                'Resumen de actividades'
            ]
            
            for columna in columnas_clave:
                valor = primer_registro.get(columna, 'N/A')
                print(f"📋 {columna}: {valor}")
            
            print("\n📊 ESTADÍSTICAS DEL PROCESAMIENTO:")
            print("-" * 40)
            
            # Contar fechas válidas
            fechas_validas = 0
            fechas_vacias = 0
            entidades = set()
            poblacion_total = 0
            
            for row in processed_data:
                fecha = row.get('Fecha final de ejecución', '')
                if fecha and fecha.strip():
                    fechas_validas += 1
                else:
                    fechas_vacias += 1
                
                entidad = row.get('Entidad', '')
                if entidad:
                    entidades.add(entidad)
                
                poblacion = row.get('Población impactada', 0)
                poblacion_total += poblacion
            
            print(f"📅 Registros con fecha válida: {fechas_validas}")
            print(f"📅 Registros sin fecha: {fechas_vacias}")
            print(f"👥 Población total impactada: {poblacion_total}")
            print(f"🏢 Entidades únicas: {len(entidades)}")
            print(f"📋 Entidades: {', '.join(sorted(entidades))}")
            
            # Simular estructura de respuesta de la API
            api_response = {
                'data': processed_data,
                'total': len(processed_data),
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"\n🌐 RESPUESTA SIMULADA DE LA API:")
            print("-" * 40)
            print(f"📊 Total de registros: {api_response['total']}")
            print(f"🕒 Última actualización: {api_response['last_update']}")
            print(f"📦 Estructura de datos: {type(api_response['data'])} con {len(api_response['data'])} elementos")
            
            return True
        else:
            print("❌ No se generaron datos procesados")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print(f"🚀 Iniciando pruebas de procesamiento API - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_data_processing()
    
    if success:
        print("\n🎯 RESULTADO FINAL: ✅ Procesamiento de datos exitoso")
        print("   La API de San Bernardo debería mostrar datos correctamente en las gráficas")
        return 0
    else:
        print("\n❌ RESULTADO FINAL: Falló el procesamiento de datos")
        print("   Revisa la configuración y el procesamiento")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
