#!/usr/bin/env python3
"""
Script para migrar reportes de la base de datos original a la nueva base de reportes-seguridad
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_modular import create_app
from models import db, Reporte, Responsable, TipoActividad, Entidad, Sector, ResultadoReporte, ArchivoReporte, User
from sqlalchemy import create_engine, text
from datetime import datetime
import logging

def migrar_reportes_railway():
    """Migrar reportes de la base original a la nueva base de reportes-seguridad"""
    
    print("🚀 Iniciando migración de reportes de Railway...")
    print("=" * 60)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Obtener la URL de la base de datos original (1000 acciones)
            from config import ProductionConfig
            database_url_original = ProductionConfig.ACCIONES_1000_DATABASE_URI
            
            if not database_url_original:
                print("❌ No se encontró ACCIONES_1000_DATABASE_URI en la configuración")
                return False
            
            print(f"✅ Conectando a base de datos original: {database_url_original.split('@')[1].split('/')[0] if '@' in database_url_original else 'N/A'}")
            
            # Conectar a la base de datos original
            engine_original = create_engine(database_url_original)
            
            with engine_original.connect() as conn_original:
                print("✅ Conectado a la base de datos original")
                
                # Buscar tablas que contengan reportes
                result = conn_original.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name LIKE '%reporte%'
                    ORDER BY table_name;
                """))
                
                reporte_tables = [row[0] for row in result]
                print(f"📊 Tablas de reportes encontradas: {reporte_tables}")
                
                if not reporte_tables:
                    print("❌ No se encontraron tablas de reportes en la base original")
                    return False
                
                # Buscar la tabla principal de reportes
                tabla_principal = None
                for table in reporte_tables:
                    if 'reporte' in table.lower() and 'participante' not in table.lower() and 'entidad' not in table.lower():
                        tabla_principal = table
                        break
                
                if not tabla_principal:
                    print("❌ No se encontró tabla principal de reportes")
                    return False
                
                print(f"📋 Usando tabla principal: {tabla_principal}")
                
                # Obtener reportes de la base original
                result = conn_original.execute(text(f"""
                    SELECT id, fecha_reporte, latitud, longitud, observaciones, 
                           responsable_id, tipo_actividad_id, sector_id, acompanamiento_juridico,
                           usuario_id, estado, fecha_actualizacion
                    FROM {tabla_principal} 
                    ORDER BY fecha_reporte DESC;
                """))
                
                reportes_originales = result.fetchall()
                print(f"📊 Reportes encontrados en base original: {len(reportes_originales)}")
                
                if len(reportes_originales) == 0:
                    print("⚠️ No hay reportes para migrar")
                    return True
                
                # Verificar cuántos reportes ya existen en la nueva base
                reportes_existentes = Reporte.query.count()
                print(f"📊 Reportes existentes en nueva base: {reportes_existentes}")
                
                # Migrar solo los reportes que no existen
                reportes_migrados = 0
                
                for reporte_data in reportes_originales:
                    # Verificar si el reporte ya existe
                    reporte_existente = Reporte.query.filter_by(id=reporte_data[0]).first()
                    
                    if reporte_existente:
                        print(f"  ⚠️ Reporte ID {reporte_data[0]} ya existe, saltando...")
                        continue
                    
                    try:
                        # Crear nuevo reporte
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
                        print(f"  ✅ Reporte ID {reporte_data[0]} agregado para migración")
                        
                    except Exception as e:
                        print(f"  ❌ Error migrando reporte ID {reporte_data[0]}: {e}")
                        continue
                
                # Buscar resultados de reportes en la base original
                tabla_resultados = f"{tabla_principal.replace('reportes', 'resultados_reporte')}"
                
                try:
                    result = conn_original.execute(text(f"""
                        SELECT id, reporte_id, cambuches_levantados, armas_blancas_decomisadas,
                               armas_fuego_decomisadas, requisas, sellamientos_establecimientos,
                               sensibilizaciones, otra_descripcion, fecha_creacion
                        FROM {tabla_resultados}
                        ORDER BY id;
                    """))
                    
                    resultados_originales = result.fetchall()
                    print(f"📊 Resultados encontrados en base original: {len(resultados_originales)}")
                    
                    # Migrar resultados
                    for resultado_data in resultados_originales:
                        resultado_existente = ResultadoReporte.query.filter_by(id=resultado_data[0]).first()
                        
                        if resultado_existente:
                            continue
                        
                        try:
                            resultado = ResultadoReporte(
                                id=resultado_data[0],
                                reporte_id=resultado_data[1],
                                cambuches_levantados=resultado_data[2] or 0,
                                armas_blancas_decomisadas=resultado_data[3] or 0,
                                armas_fuego_decomisadas=resultado_data[4] or 0,
                                requisas=resultado_data[5] or 0,
                                sellamientos_establecimientos=resultado_data[6] or 0,
                                sensibilizaciones=resultado_data[7] or 0,
                                otra_descripcion=resultado_data[8] or '',
                                fecha_creacion=resultado_data[9] if resultado_data[9] else datetime.now()
                            )
                            
                            db.session.add(resultado)
                            print(f"  ✅ Resultado ID {resultado_data[0]} agregado para migración")
                            
                        except Exception as e:
                            print(f"  ❌ Error migrando resultado ID {resultado_data[0]}: {e}")
                            continue
                
                except Exception as e:
                    print(f"⚠️ No se pudieron migrar resultados: {e}")
                
                # Guardar todos los cambios
                if reportes_migrados > 0:
                    print(f"\n💾 Guardando {reportes_migrados} reportes en la nueva base de datos...")
                    db.session.commit()
                    
                    print(f"\n🎉 ¡Migración completada exitosamente!")
                    print(f"📊 Reportes migrados: {reportes_migrados}")
                    print(f"📊 Total reportes en nueva base: {Reporte.query.count()}")
                    
                    return True
                else:
                    print("ℹ️ No se migraron reportes nuevos")
                    return True
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrar_reportes_railway()
    if success:
        print("\n✅ Migración exitosa. Los reportes ya están en la nueva base de datos.")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")

