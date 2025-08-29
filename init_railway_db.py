#!/usr/bin/env python3
"""
Script de inicialización automática para Railway
Se ejecuta al iniciar la aplicación para crear las tablas correctamente
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

def init_railway_database():
    """Inicializar base de datos de Railway automáticamente"""
    
    print("🚀 INICIALIZANDO BASE DE DATOS DE RAILWAY")
    print("=" * 50)
    
    # Obtener DATABASE_URL desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        return False
    
    try:
        # Crear conexión a la base de datos
        print("🔌 Conectando a PostgreSQL...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
        
        # Crear inspector para verificar tablas existentes
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        print(f"📊 Tablas existentes: {existing_tables}")
        
        # Verificar si necesitamos recrear actividades_1000
        if 'actividades_1000' in existing_tables:
            print("⚠️  Tabla 'actividades_1000' existe, verificando estructura...")
            
            # Verificar si la columna id es SERIAL
            columns = inspector.get_columns('actividades_1000')
            id_column = next((col for col in columns if col['name'] == 'id'), None)
            
            if id_column and 'autoincrement' in id_column and id_column['autoincrement']:
                print("✅ Tabla 'actividades_1000' tiene estructura correcta")
                
                # Verificar si existe el campo foto_base64 en fotos_actividades_1000
                if 'fotos_actividades_1000' in existing_tables:
                    foto_columns = inspector.get_columns('fotos_actividades_1000')
                    foto_base64_exists = any(col['name'] == 'foto_base64' for col in foto_columns)
                    
                    if not foto_base64_exists:
                        print("🔄 Agregando campo foto_base64 a tabla existente...")
                        with engine.connect() as connection:
                            connection.execute(text("ALTER TABLE fotos_actividades_1000 ADD COLUMN foto_base64 TEXT"))
                            connection.commit()
                        print("✅ Campo foto_base64 agregado correctamente")
                    else:
                        print("✅ Campo foto_base64 ya existe")
                
                return True
            else:
                print("❌ Tabla 'actividades_1000' tiene estructura incorrecta")
                print("🔄 Recreando tabla...")
                
                # Eliminar tabla existente
                with engine.connect() as connection:
                    connection.execute(text("DROP TABLE IF EXISTS fotos_actividades_1000 CASCADE"))
                    connection.execute(text("DROP TABLE IF EXISTS actividades_1000 CASCADE"))
                    connection.commit()
                    print("🗑️  Tablas eliminadas")
        
        # Crear tabla actividades_1000 con estructura correcta
        print("📋 Creando tabla 'actividades_1000'...")
        create_actividades_table = """
        CREATE TABLE IF NOT EXISTS actividades_1000 (
            id SERIAL PRIMARY KEY,
            nombre_responsable VARCHAR(200) NOT NULL,
            tipo_actividad VARCHAR(200) NOT NULL,
            area_responsable VARCHAR(100) NOT NULL,
            area_otro VARCHAR(200),
            personas_impactadas INTEGER NOT NULL,
            descripcion_detallada TEXT NOT NULL,
            observaciones_adicionales TEXT,
            latitud FLOAT NOT NULL,
            longitud FLOAT NOT NULL,
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(20) NOT NULL DEFAULT 'activo'
        );
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_actividades_table))
            connection.commit()
            print("✅ Tabla 'actividades_1000' creada correctamente")
        
        # Crear tabla fotos_actividades_1000
        print("📸 Creando tabla 'fotos_actividades_1000'...")
        create_fotos_table = """
        CREATE TABLE IF NOT EXISTS fotos_actividades_1000 (
            id SERIAL PRIMARY KEY,
            actividad_id INTEGER NOT NULL,
            nombre_original VARCHAR(255) NOT NULL,
            nombre_archivo VARCHAR(255) NOT NULL,
            ruta_archivo VARCHAR(500) NOT NULL,
            tipo_mime VARCHAR(100),
            tamano_bytes BIGINT,
            foto_base64 TEXT,
            fecha_subida TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (actividad_id) REFERENCES actividades_1000(id) ON DELETE CASCADE
        );
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_fotos_table))
            connection.commit()
            print("✅ Tabla 'fotos_actividades_1000' creada correctamente")
        
        # Crear tabla page_views si no existe
        if 'page_views' not in existing_tables:
            print("📊 Creando tabla 'page_views'...")
            create_page_views_table = """
            CREATE TABLE IF NOT EXISTS page_views (
                id SERIAL PRIMARY KEY,
                page_url VARCHAR(500) NOT NULL,
                user_agent TEXT,
                ip_address VARCHAR(45),
                referrer TEXT,
                session_id VARCHAR(100),
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                load_time INTEGER,
                user_id INTEGER
            );
            """
        else:
            # Si la tabla existe pero tiene estructura incorrecta, la recreamos
            print("🔄 Recreando tabla 'page_views' con estructura correcta...")
            with engine.connect() as connection:
                connection.execute(text("DROP TABLE IF EXISTS page_views CASCADE"))
                connection.commit()
                print("🗑️  Tabla 'page_views' eliminada")
            
            create_page_views_table = """
            CREATE TABLE page_views (
                id SERIAL PRIMARY KEY,
                page_url VARCHAR(500) NOT NULL,
                user_agent TEXT,
                ip_address VARCHAR(45),
                referrer TEXT,
                session_id VARCHAR(100),
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                load_time INTEGER,
                user_id INTEGER
            );
            """
            
            with engine.connect() as connection:
                connection.execute(text(create_page_views_table))
                connection.commit()
                print("✅ Tabla 'page_views' creada correctamente")
        
        # Crear índices para mejorar rendimiento
        print("🚀 Creando índices...")
        create_indices = """
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_tipo ON actividades_1000(tipo_actividad);
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_area ON actividades_1000(area_responsable);
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_fecha ON actividades_1000(fecha_creacion);
        CREATE INDEX IF NOT EXISTS idx_fotos_actividad_id ON fotos_actividades_1000(actividad_id);
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_indices))
            connection.commit()
            print("✅ Índices creados correctamente")
        
        print("\n🎉 ¡BASE DE DATOS INICIALIZADA EXITOSAMENTE!")
        print("✅ Todas las tablas creadas con estructura correcta")
        print("✅ Columna 'id' configurada como SERIAL (auto-incremento)")
        print("✅ Relaciones y índices configurados")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🏗️  INICIANDO INICIALIZACIÓN AUTOMÁTICA")
    print("=" * 50)
    
    success = init_railway_database()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Reinicia tu aplicación en Railway")
        print("2. El script se ejecutará automáticamente")
        print("3. Las tablas se crearán con estructura correcta")
        print("4. Prueba el formulario nuevamente")
    else:
        print("\n❌ La inicialización falló")
        print("Revisa los errores y vuelve a intentar")
        sys.exit(1)
