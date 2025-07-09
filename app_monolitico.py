from flask import Flask, render_template, jsonify, request, send_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import re
import xml.etree.ElementTree as ET
from io import BytesIO
import json
import tempfile
import zipfile

# Cargar variables de entorno
load_dotenv('credentials/config.env')

app = Flask(__name__)

# Configuración de Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Variables globales para almacenar datos
global_data = None
last_update = None
columns_order = None

def normalize_date(date_str):
    """
    Normaliza diferentes formatos de fecha a formato ISO (YYYY-MM-DD)
    Maneja múltiples formatos comunes en español
    """
    if not date_str or str(date_str).strip() == '':
        return None
    
    date_str = str(date_str).strip()
    
    # Si ya es un formato ISO válido, retornarlo
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    
    # Mapeo de meses en español
    meses_es = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
        'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
    }
    
    try:
        # Formato: DD/MM/YYYY o DD-MM-YYYY
        if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$', date_str):
            if '/' in date_str:
                day, month, year = date_str.split('/')
            else:
                day, month, year = date_str.split('-')
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Formato: YYYY/MM/DD o YYYY-MM-DD
        elif re.match(r'^\d{4}[/-]\d{1,2}[/-]\d{1,2}$', date_str):
            if '/' in date_str:
                year, month, day = date_str.split('/')
            else:
                year, month, day = date_str.split('-')
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Formato: DD de Mes de YYYY (ej: "15 de marzo de 2024")
        elif re.match(r'^\d{1,2}\s+de\s+[a-zA-Záéíóúñ]+\s+de\s+\d{4}$', date_str, re.IGNORECASE):
            match = re.match(r'^(\d{1,2})\s+de\s+([a-zA-Záéíóúñ]+)\s+de\s+(\d{4})$', date_str, re.IGNORECASE)
            if match:
                day, month_name, year = match.groups()
                month_name = month_name.lower()
                if month_name in meses_es:
                    month = meses_es[month_name]
                    return f"{year}-{month:02d}-{int(day):02d}"
        
        # Formato: Mes DD, YYYY (ej: "marzo 15, 2024")
        elif re.match(r'^[a-zA-Záéíóúñ]+\s+\d{1,2},\s*\d{4}$', date_str, re.IGNORECASE):
            match = re.match(r'^([a-zA-Záéíóúñ]+)\s+(\d{1,2}),\s*(\d{4})$', date_str, re.IGNORECASE)
            if match:
                month_name, day, year = match.groups()
                month_name = month_name.lower()
                if month_name in meses_es:
                    month = meses_es[month_name]
                    return f"{year}-{month:02d}-{int(day):02d}"
        
        # Formato: DD Mes YYYY (ej: "15 marzo 2024")
        elif re.match(r'^\d{1,2}\s+[a-zA-Záéíóúñ]+\s+\d{4}$', date_str, re.IGNORECASE):
            match = re.match(r'^(\d{1,2})\s+([a-zA-Záéíóúñ]+)\s+(\d{4})$', date_str, re.IGNORECASE)
            if match:
                day, month_name, year = match.groups()
                month_name = month_name.lower()
                if month_name in meses_es:
                    month = meses_es[month_name]
                    return f"{year}-{month:02d}-{int(day):02d}"
        
        # Formato: DD/MM/YY (año de 2 dígitos)
        elif re.match(r'^\d{1,2}/\d{1,2}/\d{2}$', date_str):
            day, month, year = date_str.split('/')
            # Asumir años 20xx para años de 2 dígitos
            full_year = f"20{year}" if int(year) < 50 else f"19{year}"
            return f"{full_year}-{int(month):02d}-{int(day):02d}"
        
        # Formato: DD.MM.YYYY (con puntos)
        elif re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
            day, month, year = date_str.split('.')
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Formato: DD/MM/YYYY con espacios
        elif re.match(r'^\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{4}$', date_str):
            parts = re.split(r'\s*/\s*', date_str)
            day, month, year = parts
            return f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Intentar parsear con datetime.strptime para otros formatos
        else:
            # Lista de formatos comunes a intentar
            formats = [
                '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d',
                '%d/%m/%y', '%d-%m-%y', '%Y/%m/%d', '%Y-%m-%d',
                '%d %B %Y', '%d %b %Y', '%B %d, %Y', '%b %d, %Y',
                '%d.%m.%Y', '%d.%m.%y', '%Y.%m.%d'
            ]
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        # Si no se pudo parsear, retornar None
        print(f"⚠️ No se pudo normalizar la fecha: '{date_str}'")
        return None
        
    except Exception as e:
        print(f"❌ Error normalizando fecha '{date_str}': {e}")
        return None

def process_sheet_data(data):
    """
    Procesa los datos de la hoja y normaliza las fechas
    """
    if not data:
        return data
    
    processed_data = []
    fechas_procesadas = 0
    fechas_originales = 0
    
    for i, row in enumerate(data):
        processed_row = row.copy()
        
        # Normalizar la columna de fecha final de ejecución (columna K)
        fecha_key = 'Fecha final de ejecución'
        if fecha_key in processed_row:
            fecha_original = processed_row[fecha_key]
            fecha_normalizada = normalize_date(fecha_original)
            processed_row[fecha_key] = fecha_normalizada
            
            # Contar fechas procesadas
            if fecha_original and str(fecha_original).strip() != '':
                fechas_originales += 1
                if fecha_normalizada:
                    fechas_procesadas += 1
                    print(f"✅ Fecha {i+1}: '{fecha_original}' → '{fecha_normalizada}'")
                else:
                    print(f"❌ Fecha {i+1}: '{fecha_original}' → No se pudo normalizar")
        
        processed_data.append(processed_row)
    
    print(f"\n📊 Resumen de procesamiento de fechas:")
    print(f"   Total de fechas originales: {fechas_originales}")
    print(f"   Fechas normalizadas exitosamente: {fechas_procesadas}")
    print(f"   Fechas que fallaron: {fechas_originales - fechas_procesadas}")
    
    return processed_data

def connect_to_google_sheets():
    """Conectar a Google Sheets usando credenciales de servicio"""
    try:
        # Usar credenciales de servicio (archivo JSON)
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials/credentials.json', SCOPES
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Error conectando a Google Sheets: {e}")
        return None

def fetch_data_from_sheets():
    """Obtener datos de Google Sheets"""
    global global_data, last_update, columns_order
    try:
        client = connect_to_google_sheets()
        if not client:
            print("No se pudo conectar a Google Sheets")
            return None, False
        # Abrir la hoja de cálculo
        sheet_id = os.getenv('GOOGLE_SHEET_ID', '1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU')
        sheet = client.open_by_key(sheet_id).sheet1
        # Obtener todos los datos
        raw_data = sheet.get_all_records()
        
        # Procesar y normalizar las fechas
        processed_data = process_sheet_data(raw_data)
        
        # Obtener el orden de columnas original
        columns_order = sheet.row_values(1)
        
        # Comparar con los datos actuales
        data_changed = (global_data != processed_data)
        if data_changed:
            global_data = processed_data
            last_update = datetime.now()
            print(f"Datos actualizados: {len(processed_data)} registros (cambio detectado)")
            print("Fechas normalizadas en la columna 'Fecha final de ejecución'")
        else:
            print("No hubo cambios en los datos de Google Sheets")
        return processed_data, data_changed
    except Exception as e:
        print(f"Error obteniendo datos: {e}")
        return None, False

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API para obtener datos actuales"""
    global global_data, last_update, columns_order
    
    if not global_data:
        return jsonify({'error': 'No hay datos disponibles'})
    
    return jsonify({
        'data': global_data,
        'columns_order': columns_order if 'columns_order' in globals() else list(global_data[0].keys()),
        'last_update': last_update.isoformat() if last_update else None,
        'total_records': len(global_data)
    })

@app.route('/api/refresh')
def refresh_data():
    """API para refrescar datos manualmente"""
    df, changed = fetch_data_from_sheets()
    global last_update
    if df is not None:
        return jsonify({
            'success': True,
            'message': 'Datos actualizados correctamente' if changed else 'No hubo cambios en los datos',
            'changed': changed,
            'last_update': last_update.isoformat() if last_update else None
        })
    else:
        return jsonify({'success': False, 'message': 'Error al actualizar datos', 'changed': False, 'last_update': last_update.isoformat() if last_update else None})

def schedule_data_refresh():
    """Programar actualización automática de datos"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data_from_sheets, 'interval', hours=1)
    scheduler.start()

if __name__ == '__main__':
    print("📊 Indicadores de Gestión Localidad de Santa Fé")
    print("=" * 70)
    print("🌐 Disponible en: http://localhost:5000")
    print("📋 ID de Google Sheet: 1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU")
    print("🔄 Actualización automática cada hora")
    print("=" * 70)
    
    # Cargar datos iniciales
    print("Cargando datos iniciales...")
    fetch_data_from_sheets()
    
    # Iniciar programador de actualizaciones
    schedule_data_refresh()
    
    # Ejecutar aplicación
    app.run(debug=True, host='0.0.0.0', port=5000) 