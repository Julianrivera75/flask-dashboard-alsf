#!/usr/bin/env python3
"""
Script para crear las tablas en la base de datos de Railway
"""

import os
import psycopg2
from urllib.parse import urlparse

def crear_tablas_railway():
    """
    Crea las tablas necesarias en la base de datos de Railway
    """
    print("🚀 Creando tablas en Railway PostgreSQL...")
    print("=" * 50)
    
    # Solicitar la URL de la base de datos
    database_url = input("Ingresa la URL de la base de datos de Railway (DATABASE_URL): ").strip()
    
    if not database_url:
        print("❌ No se proporcionó la URL de la base de datos")
        return False
    
    try:
        # Parsear la URL
        parsed = urlparse(database_url)
        
        print(f"🔗 Conectando a Railway PostgreSQL...")
        print(f"   Host: {parsed.hostname}")
        print(f"   Puerto: {parsed.port}")
        print(f"   Base de datos: {parsed.path[1:]}")
        print(f"   Usuario: {parsed.username}")
        
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a Railway PostgreSQL")
        
        # Crear tabla de usuarios
        print("📋 Creando tabla de usuarios...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de responsables
        print("📋 Creando tabla de responsables...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responsables (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                cargo VARCHAR(100),
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de tipos de actividad
        print("📋 Creando tabla de tipos de actividad...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_actividad (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de sectores
        print("📋 Creando tabla de sectores...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sectores (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de entidades
        print("📋 Creando tabla de entidades...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entidades (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de reportes
        print("📋 Creando tabla de reportes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reportes (
                id SERIAL PRIMARY KEY,
                fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responsable_id INTEGER,
                latitud FLOAT NOT NULL,
                longitud FLOAT NOT NULL,
                sector_id INTEGER,
                tipo_actividad_id INTEGER,
                acompanamiento_juridico BOOLEAN DEFAULT FALSE,
                observaciones TEXT,
                usuario_id INTEGER NOT NULL,
                estado VARCHAR(20) DEFAULT 'activo',
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de resultados de reporte
        print("📋 Creando tabla de resultados de reporte...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_reporte (
                id SERIAL PRIMARY KEY,
                reporte_id INTEGER,
                cambuches_levantados INTEGER DEFAULT 0,
                armas_blancas_decomisadas INTEGER DEFAULT 0,
                armas_fuego_decomisadas INTEGER DEFAULT 0,
                requisas INTEGER DEFAULT 0,
                sellamientos_establecimientos INTEGER DEFAULT 0,
                sensibilizaciones INTEGER DEFAULT 0,
                otra_descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de archivos de reporte
        print("📋 Creando tabla de archivos de reporte...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archivos_reporte (
                id SERIAL PRIMARY KEY,
                reporte_id INTEGER,
                nombre_archivo VARCHAR(255) NOT NULL,
                ruta_archivo VARCHAR(500) NOT NULL,
                tipo_archivo VARCHAR(50),
                tamaño_archivo INTEGER,
                fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de analytics
        print("📋 Creando tabla de analytics...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                id SERIAL PRIMARY KEY,
                page_url VARCHAR(500) NOT NULL,
                user_agent TEXT,
                ip_address VARCHAR(45),
                referrer VARCHAR(500),
                session_id VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                load_time FLOAT,
                user_id INTEGER
            );
        """)
        
        # Crear usuario administrador
        print("👤 Creando usuario administrador...")
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, is_admin) 
            VALUES ('admin_reportes', 'admin.reportes@alsf.gov.co', 'scrypt:32768:8:1$2b$12$...', TRUE)
            ON CONFLICT (username) DO NOTHING;
        """)
        
        # Crear tipos de actividad de ejemplo
        print("📋 Creando tipos de actividad de ejemplo...")
        tipos_ejemplo = [
            ('Patrullaje', 'Actividades de patrullaje y vigilancia'),
            ('Operativo', 'Operativos de seguridad y convivencia'),
            ('Sensibilización', 'Actividades de sensibilización comunitaria'),
            ('Intervención', 'Intervenciones en puntos críticos'),
            ('Requisas', 'Actividades de requisa y decomiso'),
            ('Levantamiento', 'Levantamiento de cambuches'),
            ('Sellamiento', 'Sellamiento de establecimientos'),
            ('Acompañamiento', 'Acompañamiento jurídico y social')
        ]
        
        for nombre, descripcion in tipos_ejemplo:
            cursor.execute("""
                INSERT INTO tipos_actividad (nombre, descripcion) 
                VALUES (%s, %s)
                ON CONFLICT (nombre) DO NOTHING;
            """, (nombre, descripcion))
        
        # Crear sectores de ejemplo
        print("📋 Creando sectores de ejemplo...")
        sectores_ejemplo = [
            ('Centro', 'Sector centro de Santa Fe'),
            ('Norte', 'Sector norte de Santa Fe'),
            ('Sur', 'Sector sur de Santa Fe'),
            ('Oriente', 'Sector oriente de Santa Fe'),
            ('Occidente', 'Sector occidente de Santa Fe')
        ]
        
        for nombre, descripcion in sectores_ejemplo:
            cursor.execute("""
                INSERT INTO sectores (nombre, descripcion) 
                VALUES (%s, %s)
                ON CONFLICT (nombre) DO NOTHING;
            """, (nombre, descripcion))
        
        # Confirmar cambios
        conn.commit()
        
        print("✅ Todas las tablas creadas exitosamente en Railway")
        print("✅ Usuario administrador creado: admin_reportes")
        print("✅ Tipos de actividad de ejemplo creados")
        print("✅ Sectores de ejemplo creados")
        
        # Verificar tablas creadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 Tablas creadas ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Configuración de Railway completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Configuración de Base de Datos Railway")
    print("Este script creará las tablas necesarias para 'Santa Fe Camina Segura'")
    print()
    
    success = crear_tablas_railway()
    
    if success:
        print("\n✅ ¡Listo! Ahora puedes desplegar tu aplicación en Railway.")
        print("📋 La base de datos está configurada y lista para recibir reportes.")
    else:
        print("\n❌ Hubo un error. Revisa la URL de la base de datos e intenta de nuevo.")