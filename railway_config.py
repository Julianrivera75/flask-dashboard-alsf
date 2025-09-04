"""
Configuración específica para Railway
"""
import os
import psycopg2
from urllib.parse import urlparse

def get_railway_database_url():
    """
    Obtiene la URL de la base de datos de Railway
    Railway proporciona automáticamente la variable DATABASE_URL
    """
    return os.environ.get('DATABASE_URL')

def parse_database_url(database_url):
    """
    Parsea la URL de la base de datos de Railway
    """
    if not database_url:
        return None
    
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port,
        'database': parsed.path[1:],  # Remover el '/' inicial
        'user': parsed.username,
        'password': parsed.password,
        'sslmode': 'require'  # Railway requiere SSL
    }

def test_railway_connection():
    """
    Prueba la conexión a la base de datos de Railway
    """
    database_url = get_railway_database_url()
    if not database_url:
        print("❌ No se encontró DATABASE_URL en las variables de entorno")
        return False
    
    try:
        conn_params = parse_database_url(database_url)
        if not conn_params:
            print("❌ Error al parsear la URL de la base de datos")
            return False
        
        print("🔗 Conectando a Railway PostgreSQL...")
        print(f"   Host: {conn_params['host']}")
        print(f"   Puerto: {conn_params['port']}")
        print(f"   Base de datos: {conn_params['database']}")
        print(f"   Usuario: {conn_params['user']}")
        
        # Probar conexión
        conn = psycopg2.connect(
            host=conn_params['host'],
            port=conn_params['port'],
            database=conn_params['database'],
            user=conn_params['user'],
            password=conn_params['password'],
            sslmode=conn_params['sslmode']
        )
        
        # Probar consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ Conexión exitosa a Railway PostgreSQL")
        print(f"   Versión: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def create_railway_tables():
    """
    Crea las tablas necesarias en Railway
    """
    database_url = get_railway_database_url()
    if not database_url:
        print("❌ No se encontró DATABASE_URL")
        return False
    
    try:
        conn_params = parse_database_url(database_url)
        conn = psycopg2.connect(
            host=conn_params['host'],
            port=conn_params['port'],
            database=conn_params['database'],
            user=conn_params['user'],
            password=conn_params['password'],
            sslmode=conn_params['sslmode']
        )
        
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
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
        
        # Crear tabla de reportes
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
        
        # Crear tabla de responsables
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entidades (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de resultados de reporte
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
        
        conn.commit()
        print("✅ Tablas creadas exitosamente en Railway")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear tablas: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando base de datos en Railway...")
    print("=" * 50)
    
    # Probar conexión
    if test_railway_connection():
        print("\n📋 Creando tablas...")
        if create_railway_tables():
            print("\n✅ Configuración de Railway completada exitosamente!")
        else:
            print("\n❌ Error al crear las tablas")
    else:
        print("\n❌ No se pudo conectar a Railway")
