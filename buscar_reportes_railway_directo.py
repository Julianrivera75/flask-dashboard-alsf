#!/usr/bin/env python3
"""
Script para buscar reportes en la base de datos original de Railway
Se ejecuta directamente en Railway
"""

import os
import sys
from sqlalchemy import create_engine, text

def buscar_reportes_railway_directo():
    """Buscar reportes en la base de datos original de Railway"""
    
    print("🔍 Buscando reportes en la base de datos original de Railway...")
    print("=" * 60)
    
    # URL de la base de datos original (1000 acciones)
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ No se encontró DATABASE_URL en las variables de entorno")
        print("   Este script debe ejecutarse en Railway")
        return
    
    try:
        # Conectar a la base de datos original
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Conectado a la base de datos original de Railway")
            print(f"   Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'N/A'}")
            
            # Verificar qué tablas existen
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"\n📊 Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table}")
            
            # Buscar tablas que puedan contener reportes
            reporte_tables = [t for t in tables if 'reporte' in t.lower()]
            
            if reporte_tables:
                print(f"\n🔍 Tablas relacionadas con reportes: {reporte_tables}")
                
                for table in reporte_tables:
                    # Contar registros
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table};"))
                    count = result.scalar()
                    print(f"  - {table}: {count} registros")
                    
                    # Si hay registros, mostrar algunos
                    if count > 0:
                        result = conn.execute(text(f"SELECT * FROM {table} LIMIT 3;"))
                        rows = result.fetchall()
                        print(f"    Primeros registros:")
                        for i, row in enumerate(rows, 1):
                            print(f"      {i}. {row}")
                        
                        # Si es la tabla de reportes, mostrar detalles
                        if 'reporte' in table.lower() and 'participante' not in table.lower() and 'entidad' not in table.lower():
                            print(f"\n📋 Detalles de reportes en {table}:")
                            result = conn.execute(text(f"""
                                SELECT id, fecha_reporte, latitud, longitud, observaciones, responsable_id, tipo_actividad_id, sector_id
                                FROM {table} 
                                ORDER BY fecha_reporte DESC
                                LIMIT 10;
                            """))
                            
                            reportes = result.fetchall()
                            for i, reporte in enumerate(reportes, 1):
                                print(f"  {i}. ID: {reporte[0]}")
                                print(f"     Fecha: {reporte[1]}")
                                print(f"     Coordenadas: ({reporte[2]}, {reporte[3]})")
                                print(f"     Observaciones: {reporte[4][:50]}..." if reporte[4] else "     Observaciones: None")
                                print(f"     Responsable ID: {reporte[5]}")
                                print(f"     Tipo Actividad ID: {reporte[6]}")
                                print(f"     Sector ID: {reporte[7]}")
                                print()
            else:
                print("\n⚠️ No se encontraron tablas relacionadas con reportes")
                
                # Buscar en todas las tablas por registros que puedan ser reportes
                print("\n🔍 Buscando datos en todas las tablas...")
                for table in tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table};"))
                        count = result.scalar()
                        if count > 0:
                            print(f"  - {table}: {count} registros")
                            
                            # Mostrar estructura de la tabla
                            result = conn.execute(text(f"""
                                SELECT column_name, data_type 
                                FROM information_schema.columns 
                                WHERE table_name = '{table}'
                                ORDER BY ordinal_position;
                            """))
                            columns = result.fetchall()
                            print(f"    Columnas: {[col[0] for col in columns]}")
                            
                            # Si tiene coordenadas, podría ser reportes
                            column_names = [col[0] for col in columns]
                            if 'latitud' in column_names and 'longitud' in column_names:
                                print(f"    ⚠️  Esta tabla tiene coordenadas - podría contener reportes!")
                                
                                # Mostrar algunos registros con coordenadas
                                result = conn.execute(text(f"""
                                    SELECT * FROM {table} 
                                    WHERE latitud IS NOT NULL AND longitud IS NOT NULL
                                    LIMIT 3;
                                """))
                                rows = result.fetchall()
                                print(f"    Registros con coordenadas:")
                                for i, row in enumerate(rows, 1):
                                    print(f"      {i}. {row}")
                            
                    except Exception as e:
                        print(f"  - {table}: Error al consultar - {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    buscar_reportes_railway_directo()
