#!/usr/bin/env python3
"""
Script para crear las tablas de Acciones 1000 en PostgreSQL de Railway
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def crear_tablas_acciones_1000():
    """Crear las tablas necesarias para Acciones 1000"""
    
    # Obtener la URL de la base de datos desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        print("Asegúrate de que esté configurada en Railway")
        return False
    
    try:
        # Crear conexión a la base de datos
        print("🔌 Conectando a la base de datos...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
        
        # Crear tabla actividades_1000
        print("📋 Creando tabla actividades_1000...")
        crear_tabla_actividades = """
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
            connection.execute(text(crear_tabla_actividades))
            connection.commit()
            print("✅ Tabla actividades_1000 creada exitosamente")
        
        # Crear tabla fotos_actividades_1000
        print("📸 Creando tabla fotos_actividades_1000...")
        crear_tabla_fotos = """
        CREATE TABLE IF NOT EXISTS fotos_actividades_1000 (
            id SERIAL PRIMARY KEY,
            actividad_id INTEGER NOT NULL,
            nombre_original VARCHAR(255) NOT NULL,
            nombre_archivo VARCHAR(255) NOT NULL,
            ruta_archivo VARCHAR(500) NOT NULL,
            tipo_mime VARCHAR(100),
            tamano_bytes BIGINT,
            fecha_subida TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (actividad_id) REFERENCES actividades_1000(id) ON DELETE CASCADE
        );
        """
        
        with engine.connect() as connection:
            connection.execute(text(crear_tabla_fotos))
            connection.commit()
            print("✅ Tabla fotos_actividades_1000 creada exitosamente")
        
        # Crear índices para mejorar rendimiento
        print("🚀 Creando índices...")
        crear_indices = """
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_tipo ON actividades_1000(tipo_actividad);
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_area ON actividades_1000(area_responsable);
        CREATE INDEX IF NOT EXISTS idx_actividades_1000_fecha ON actividades_1000(fecha_creacion);
        CREATE INDEX IF NOT EXISTS idx_fotos_actividad_id ON fotos_actividades_1000(actividad_id);
        """
        
        with engine.connect() as connection:
            connection.execute(text(crear_indices))
            connection.commit()
            print("✅ Índices creados exitosamente")
        
        print("\n🎉 ¡TABLAS CREADAS EXITOSAMENTE!")
        print("✅ actividades_1000")
        print("✅ fotos_actividades_1000")
        print("✅ Índices de rendimiento")
        print("\n🚀 Ahora puedes probar el formulario en Railway")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🏗️  CREANDO TABLAS PARA ACCIONES 1000 EN RAILWAY")
    print("=" * 50)
    
    success = crear_tablas_acciones_1000()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ve a tu aplicación en Railway")
        print("2. Prueba el formulario de registro")
        print("3. Verifica que se guarde la actividad")
        print("4. Revisa el mapa de actividades")
    else:
        print("\n❌ No se pudieron crear las tablas")
        print("Revisa los errores y vuelve a intentar")
        sys.exit(1)
