#!/usr/bin/env python3
"""
Script simple para probar la conexión a la base de datos de Railway
"""

import os
import psycopg2
from psycopg2 import Error

def test_railway_connection():
    """Probar conexión directa a PostgreSQL de Railway"""
    
    print("🔌 PROBANDO CONEXIÓN A RAILWAY POSTGRESQL")
    print("=" * 50)
    
    # Obtener DATABASE_URL desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        print("Configura esta variable en tu entorno local:")
        print("set DATABASE_URL=${{ acciones-1000-db.DATABASE_URL }}")
        return False
    
    print(f"📡 Conectando a: {database_url[:50]}...")
    
    try:
        # Conectar usando psycopg2 directamente
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()
        
        print("✅ Conexión exitosa a PostgreSQL")
        
        # Verificar que las tablas existen
        print("\n📋 Verificando tablas...")
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar estructura de actividades_1000
        if ('actividades_1000',) in tables:
            print("\n🔍 Verificando estructura de 'actividades_1000'...")
            
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'actividades_1000'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print(f"📋 Columnas en 'actividades_1000': {len(columns)}")
            
            for col in columns:
                nullable = "NOT NULL" if col[2] == "NO" else "NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  - {col[0]}: {col[1]} {nullable}{default}")
        
        # Verificar estructura de fotos_actividades_1000
        if ('fotos_actividades_1000',) in tables:
            print("\n🔍 Verificando estructura de 'fotos_actividades_1000'...")
            
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'fotos_actividades_1000'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print(f"📋 Columnas en 'fotos_actividades_1000': {len(columns)}")
            
            for col in columns:
                nullable = "NOT NULL" if col[2] == "NO" else "NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  - {col[0]}: {col[1]} {nullable}{default}")
        
        # Probar inserción simple
        print("\n🧪 Probando inserción simple...")
        
        try:
            cursor.execute("""
                INSERT INTO actividades_1000 (
                    nombre_responsable, tipo_actividad, area_responsable,
                    personas_impactadas, descripcion_detallada,
                    latitud, longitud, estado
                ) VALUES (
                    'Test User', 'DANZA', 'Deportes',
                    10, 'Prueba de conexión',
                    4.584197, -74.075972, 'activo'
                ) RETURNING id;
            """)
            
            new_id = cursor.fetchone()[0]
            print(f"✅ Inserción exitosa! ID: {new_id}")
            
            # Limpiar prueba
            cursor.execute("DELETE FROM actividades_1000 WHERE id = %s", (new_id,))
            print("🧹 Registro de prueba eliminado")
            
        except Exception as e:
            print(f"❌ Error en inserción: {e}")
        
        cursor.close()
        connection.close()
        print("\n🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
        
        return True
        
    except Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CONEXIÓN A RAILWAY")
    print("=" * 50)
    
    success = test_railway_connection()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Si la prueba pasó, el problema está en la aplicación Flask")
        print("2. Si la prueba falló, el problema está en la base de datos")
        print("3. Revisa los logs de Railway para más detalles")
    else:
        print("\n❌ La conexión falló")
        print("Verifica la configuración de DATABASE_URL")
