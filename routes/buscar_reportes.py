#!/usr/bin/env python3
"""
Ruta para buscar reportes perdidos en Railway
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, text
import os
import logging

buscar_reportes_bp = Blueprint('buscar_reportes', __name__)

@buscar_reportes_bp.route('/buscar-reportes-perdidos')
def buscar_reportes_perdidos():
    """Buscar reportes perdidos en la base de datos original de Railway"""
    
    try:
        # URL de la base de datos original (1000 acciones)
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            return jsonify({
                'error': 'No se encontró DATABASE_URL en las variables de entorno',
                'success': False
            }), 500
        
        # Conectar a la base de datos original
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            logging.info("🔍 Buscando reportes en la base de datos original de Railway...")
            
            # Verificar qué tablas existen
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            logging.info(f"📊 Tablas encontradas: {len(tables)}")
            
            # Buscar tablas que puedan contener reportes
            reporte_tables = [t for t in tables if 'reporte' in t.lower()]
            
            reportes_encontrados = []
            
            if reporte_tables:
                logging.info(f"🔍 Tablas relacionadas con reportes: {reporte_tables}")
                
                for table in reporte_tables:
                    # Contar registros
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table};"))
                    count = result.scalar()
                    logging.info(f"  - {table}: {count} registros")
                    
                    # Si hay registros, obtener los datos
                    if count > 0:
                        # Si es la tabla de reportes, obtener detalles
                        if 'reporte' in table.lower() and 'participante' not in table.lower() and 'entidad' not in table.lower():
                            result = conn.execute(text(f"""
                                SELECT id, fecha_reporte, latitud, longitud, observaciones, responsable_id, tipo_actividad_id, sector_id
                                FROM {table} 
                                ORDER BY fecha_reporte DESC
                                LIMIT 20;
                            """))
                            
                            reportes = result.fetchall()
                            for reporte in reportes:
                                reportes_encontrados.append({
                                    'id': reporte[0],
                                    'fecha_reporte': str(reporte[1]) if reporte[1] else None,
                                    'latitud': float(reporte[2]) if reporte[2] else None,
                                    'longitud': float(reporte[3]) if reporte[3] else None,
                                    'observaciones': reporte[4],
                                    'responsable_id': reporte[5],
                                    'tipo_actividad_id': reporte[6],
                                    'sector_id': reporte[7],
                                    'tabla_origen': table
                                })
            else:
                logging.info("⚠️ No se encontraron tablas relacionadas con reportes")
                
                # Buscar en todas las tablas por registros que puedan ser reportes
                logging.info("🔍 Buscando datos en todas las tablas...")
                for table in tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table};"))
                        count = result.scalar()
                        if count > 0:
                            # Mostrar estructura de la tabla
                            result = conn.execute(text(f"""
                                SELECT column_name, data_type 
                                FROM information_schema.columns 
                                WHERE table_name = '{table}'
                                ORDER BY ordinal_position;
                            """))
                            columns = result.fetchall()
                            column_names = [col[0] for col in columns]
                            
                            # Si tiene coordenadas, podría ser reportes
                            if 'latitud' in column_names and 'longitud' in column_names:
                                logging.info(f"⚠️  {table} tiene coordenadas - podría contener reportes!")
                                
                                # Obtener registros con coordenadas
                                result = conn.execute(text(f"""
                                    SELECT * FROM {table} 
                                    WHERE latitud IS NOT NULL AND longitud IS NOT NULL
                                    LIMIT 10;
                                """))
                                rows = result.fetchall()
                                
                                for row in rows:
                                    # Intentar mapear a estructura de reporte
                                    reporte_data = {
                                        'tabla_origen': table,
                                        'datos_raw': dict(zip(column_names, row))
                                    }
                                    
                                    # Buscar campos comunes
                                    for i, col in enumerate(column_names):
                                        if 'id' in col.lower() and reporte_data.get('id') is None:
                                            reporte_data['id'] = row[i]
                                        elif 'fecha' in col.lower() and reporte_data.get('fecha_reporte') is None:
                                            reporte_data['fecha_reporte'] = str(row[i]) if row[i] else None
                                        elif col.lower() == 'latitud':
                                            reporte_data['latitud'] = float(row[i]) if row[i] else None
                                        elif col.lower() == 'longitud':
                                            reporte_data['longitud'] = float(row[i]) if row[i] else None
                                        elif 'observacion' in col.lower() or 'descripcion' in col.lower():
                                            reporte_data['observaciones'] = row[i]
                                    
                                    reportes_encontrados.append(reporte_data)
                                
                    except Exception as e:
                        logging.error(f"  - {table}: Error al consultar - {e}")
            
            return jsonify({
                'success': True,
                'total_tablas': len(tables),
                'tablas_reportes': reporte_tables,
                'total_reportes_encontrados': len(reportes_encontrados),
                'reportes': reportes_encontrados,
                'database_url': database_url.split('@')[1].split('/')[0] if '@' in database_url else 'N/A'
            })
            
    except Exception as e:
        logging.error(f"❌ Error buscando reportes perdidos: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
