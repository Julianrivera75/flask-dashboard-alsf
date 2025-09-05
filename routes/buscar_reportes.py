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

@buscar_reportes_bp.route('/migrar-reportes-perdidos')
def migrar_reportes_perdidos():
    """Migrar reportes perdidos de la base original a la nueva base de reportes-seguridad"""
    
    try:
        from app_modular import create_app
        from models import db, Reporte, ResultadoReporte
        from sqlalchemy import create_engine, text
        from datetime import datetime
        import os
        
        app = create_app()
        
        with app.app_context():
            # Obtener la URL de la base de datos original
            from config import ProductionConfig
            database_url_original = ProductionConfig.ACCIONES_1000_DATABASE_URI
            
            if not database_url_original:
                return jsonify({
                    'error': 'No se encontró ACCIONES_1000_DATABASE_URI',
                    'success': False
                }), 500
            
            # Conectar a la base de datos original
            engine_original = create_engine(database_url_original)
            
            with engine_original.connect() as conn_original:
                logging.info("🔍 Buscando reportes en base original...")
                
                # Buscar tabla de reportes
                result = conn_original.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name LIKE '%reporte%'
                    AND table_name NOT LIKE '%participante%'
                    AND table_name NOT LIKE '%entidad%'
                    ORDER BY table_name;
                """))
                
                reporte_tables = [row[0] for row in result]
                
                if not reporte_tables:
                    return jsonify({
                        'error': 'No se encontraron tablas de reportes en la base original',
                        'success': False
                    }), 500
                
                tabla_principal = reporte_tables[0]
                logging.info(f"📋 Usando tabla: {tabla_principal}")
                
                # Obtener reportes de la base original
                result = conn_original.execute(text(f"""
                    SELECT id, fecha_reporte, latitud, longitud, observaciones, 
                           responsable_id, tipo_actividad_id, sector_id, acompanamiento_juridico,
                           usuario_id, estado, fecha_actualizacion
                    FROM {tabla_principal} 
                    ORDER BY fecha_reporte DESC;
                """))
                
                reportes_originales = result.fetchall()
                logging.info(f"📊 Reportes encontrados: {len(reportes_originales)}")
                
                # Verificar cuántos ya existen
                reportes_existentes = Reporte.query.count()
                logging.info(f"📊 Reportes existentes en nueva base: {reportes_existentes}")
                
                # Migrar reportes
                reportes_migrados = 0
                errores = []
                
                for reporte_data in reportes_originales:
                    # Verificar si ya existe
                    if Reporte.query.filter_by(id=reporte_data[0]).first():
                        continue
                    
                    try:
                        reporte = Reporte(
                            id=reporte_data[0],
                            fecha_reporte=reporte_data[1],
                            latitud=reporte_data[2],
                            longitud=reporte_data[3],
                            observaciones=reporte_data[4],
                            responsable_id=reporte_data[5],
                            tipo_actividad_id=reporte_data[6],
                            sector_id=reporte_data[7],
                            acompanamiento_juridico=reporte_data[8] == 1 if reporte_data[8] is not None else False,
                            usuario_id=reporte_data[9] if reporte_data[9] else 1,
                            estado=reporte_data[10] if reporte_data[10] else 'activo',
                            fecha_actualizacion=reporte_data[11] if reporte_data[11] else datetime.now()
                        )
                        
                        db.session.add(reporte)
                        reportes_migrados += 1
                        logging.info(f"✅ Reporte ID {reporte_data[0]} agregado")
                        
                    except Exception as e:
                        errores.append(f"Error migrando reporte ID {reporte_data[0]}: {str(e)}")
                        logging.error(f"❌ Error migrando reporte ID {reporte_data[0]}: {e}")
                
                # Guardar cambios
                if reportes_migrados > 0:
                    db.session.commit()
                    logging.info(f"💾 {reportes_migrados} reportes migrados exitosamente")
                
                return jsonify({
                    'success': True,
                    'reportes_encontrados': len(reportes_originales),
                    'reportes_migrados': reportes_migrados,
                    'reportes_existentes_antes': reportes_existentes,
                    'reportes_totales_ahora': Reporte.query.count(),
                    'errores': errores,
                    'tabla_origen': tabla_principal
                })
                
    except Exception as e:
        logging.error(f"❌ Error en migración: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@buscar_reportes_bp.route('/diagnosticar-reportes')
def diagnosticar_reportes():
    """Diagnosticar problemas con reportes en Railway"""
    
    try:
        from app_modular import create_app
        from models import db, Reporte, Responsable, TipoActividad, Entidad, Sector, ResultadoReporte
        from sqlalchemy import create_engine, text
        import os
        
        app = create_app()
        
        with app.app_context():
            logging.info("🔍 Iniciando diagnóstico de reportes...")
            
            # 1. Verificar configuración de bases de datos
            from config import ProductionConfig
            config_info = {
                'sqlalchemy_database_uri': ProductionConfig.SQLALCHEMY_DATABASE_URI[:50] + "..." if ProductionConfig.SQLALCHEMY_DATABASE_URI else "No configurado",
                'acciones_1000_database_uri': ProductionConfig.ACCIONES_1000_DATABASE_URI[:50] + "..." if ProductionConfig.ACCIONES_1000_DATABASE_URI else "No configurado"
            }
            
            # 2. Verificar reportes en la nueva base de datos
            reportes_nueva = Reporte.query.all()
            reportes_info = []
            
            for reporte in reportes_nueva:
                reportes_info.append({
                    'id': reporte.id,
                    'fecha_reporte': str(reporte.fecha_reporte) if reporte.fecha_reporte else None,
                    'latitud': reporte.latitud,
                    'longitud': reporte.longitud,
                    'observaciones': reporte.observaciones
                })
            
            # 3. Verificar reportes en la base de datos original
            reportes_originales = []
            tabla_original = None
            
            try:
                if ProductionConfig.ACCIONES_1000_DATABASE_URI:
                    engine_original = create_engine(ProductionConfig.ACCIONES_1000_DATABASE_URI)
                    
                    with engine_original.connect() as conn:
                        # Buscar tablas de reportes
                        result = conn.execute(text("""
                            SELECT table_name 
                            FROM information_schema.tables 
                            WHERE table_schema = 'public'
                            AND table_name LIKE '%reporte%'
                            ORDER BY table_name;
                        """))
                        
                        reporte_tables = [row[0] for row in result]
                        
                        if reporte_tables:
                            # Buscar la tabla principal
                            for table in reporte_tables:
                                if 'reporte' in table.lower() and 'participante' not in table.lower() and 'entidad' not in table.lower():
                                    tabla_original = table
                                    break
                            
                            if tabla_original:
                                # Obtener reportes
                                result = conn.execute(text(f"""
                                    SELECT id, fecha_reporte, latitud, longitud, observaciones
                                    FROM {tabla_original} 
                                    ORDER BY fecha_reporte DESC
                                    LIMIT 10;
                                """))
                                
                                for row in result:
                                    reportes_originales.append({
                                        'id': row[0],
                                        'fecha_reporte': str(row[1]) if row[1] else None,
                                        'latitud': row[2],
                                        'longitud': row[3],
                                        'observaciones': row[4]
                                    })
                                
            except Exception as e:
                logging.error(f"Error conectando a base original: {e}")
            
            # 4. Verificar otras tablas
            otras_tablas = {
                'responsables': Responsable.query.count(),
                'tipos_actividad': TipoActividad.query.count(),
                'entidades': Entidad.query.count(),
                'sectores': Sector.query.count(),
                'resultados': ResultadoReporte.query.count()
            }
            
            # 5. Verificar variables de entorno
            env_vars = {
                'FLASK_ENV': os.environ.get('FLASK_ENV', 'No configurado'),
                'REPORTES_DATABASE_URL': 'Configurado' if os.environ.get('REPORTES_DATABASE_URL') else 'No configurado',
                'DATABASE_URL': 'Configurado' if os.environ.get('DATABASE_URL') else 'No configurado'
            }
            
            return jsonify({
                'success': True,
                'configuracion': config_info,
                'reportes_nueva_base': {
                    'total': len(reportes_nueva),
                    'reportes': reportes_info
                },
                'reportes_base_original': {
                    'total': len(reportes_originales),
                    'tabla': tabla_original,
                    'reportes': reportes_originales
                },
                'otras_tablas': otras_tablas,
                'variables_entorno': env_vars
            })
            
    except Exception as e:
        logging.error(f"❌ Error en diagnóstico: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
