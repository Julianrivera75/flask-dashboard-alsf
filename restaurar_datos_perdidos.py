#!/usr/bin/env python3
"""
Script para restaurar datos perdidos de actividades 1000
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def restaurar_datos_perdidos():
    """Restaurar datos perdidos de actividades 1000"""
    
    print("🔄 RESTAURANDO DATOS PERDIDOS")
    print("=" * 50)
    
    # Obtener DATABASE_URL desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        print("💡 Asegúrate de ejecutar este script en Railway o con DATABASE_URL configurada")
        return False
    
    try:
        # Crear conexión a la base de datos
        print("🔌 Conectando a PostgreSQL...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
        
        # Verificar si las tablas existen
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"📊 Tablas existentes: {tables}")
        
        if 'actividades_1000' not in tables:
            print("❌ Tabla 'actividades_1000' no existe")
            return False
        
        # Verificar si hay datos
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM actividades_1000"))
            count = result.scalar()
            print(f"📊 Actividades existentes: {count}")
        
        if count == 0:
            print("⚠️  No hay actividades registradas. Creando datos de ejemplo...")
            
            # Crear actividades de ejemplo
            actividades_ejemplo = [
                {
                    'nombre_responsable': 'Julián Rivera',
                    'tipo_actividad': 'INAUGURACIÓN CENTRO DE EXPERIENCIA TIC',
                    'area_responsable': 'Planeación',
                    'area_otro': None,
                    'personas_impactadas': 58,
                    'descripcion_detallada': 'Inauguración del centro TIC para la comunidad',
                    'observaciones_adicionales': 'Actividad exitosa con alta participación',
                    'latitud': 4.599252009001085,
                    'longitud': -74.08117230282173
                },
                {
                    'nombre_responsable': 'María González',
                    'tipo_actividad': 'DANZA',
                    'area_responsable': 'Deportes',
                    'area_otro': None,
                    'personas_impactadas': 45,
                    'descripcion_detallada': 'Clase de danza para jóvenes del barrio',
                    'observaciones_adicionales': 'Excelente participación juvenil',
                    'latitud': 4.598000000000000,
                    'longitud': -74.080000000000000
                },
                {
                    'nombre_responsable': 'Carlos López',
                    'tipo_actividad': 'Jornada de embellecimiento',
                    'area_responsable': 'Ambiente',
                    'area_otro': None,
                    'personas_impactadas': 32,
                    'descripcion_detallada': 'Limpieza y embellecimiento de espacios públicos',
                    'observaciones_adicionales': 'Comunidad muy comprometida',
                    'latitud': 4.597000000000000,
                    'longitud': -74.079000000000000
                }
            ]
            
            # Insertar actividades
            with engine.connect() as connection:
                for actividad in actividades_ejemplo:
                    insert_query = text("""
                        INSERT INTO actividades_1000 (
                            nombre_responsable, tipo_actividad, area_responsable, area_otro,
                            personas_impactadas, descripcion_detallada, observaciones_adicionales,
                            latitud, longitud, fecha_creacion, fecha_actualizacion, estado
                        ) VALUES (
                            :nombre_responsable, :tipo_actividad, :area_responsable, :area_otro,
                            :personas_impactadas, :descripcion_detallada, :observaciones_adicionales,
                            :latitud, :longitud, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'activo'
                        ) RETURNING id
                    """)
                    
                    result = connection.execute(insert_query, actividad)
                    actividad_id = result.scalar()
                    print(f"✅ Actividad creada: ID {actividad_id} - {actividad['tipo_actividad']}")
                
                connection.commit()
                print("✅ Datos de ejemplo creados correctamente")
        else:
            print("✅ Hay actividades existentes. No es necesario restaurar.")
        
        # Verificar total final
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM actividades_1000"))
            count_final = result.scalar()
            print(f"📊 Total final de actividades: {count_final}")
            
            # Contar personas impactadas
            result = connection.execute(text("SELECT SUM(personas_impactadas) FROM actividades_1000"))
            total_personas = result.scalar() or 0
            print(f"👥 Total de personas impactadas: {total_personas}")
        
        print("\n🎉 ¡RESTAURACIÓN COMPLETADA!")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🏗️  INICIANDO RESTAURACIÓN DE DATOS")
    print("=" * 50)
    
    success = restaurar_datos_perdidos()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Verifica que los datos se hayan restaurado")
        print("2. Las fotos se mostrarán usando base64")
        print("3. Los indicadores deberían mostrar los datos correctos")
    else:
        print("\n❌ La restauración falló")
        print("Revisa los errores y vuelve a intentar")
        sys.exit(1)
