#!/usr/bin/env python3
"""
Script para inicializar la base de datos de 1000 Acciones en 1 Día
"""

import os
import sys
import logging
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app, db
from models.acciones_1000 import create_acciones_1000_models
from config import DevelopmentConfig

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_acciones_1000_database():
    """Inicializar la base de datos para 1000 Acciones en 1 Día"""
    
    try:
        # Crear aplicación
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            logger.info("🔄 Inicializando base de datos para 1000 Acciones en 1 Día...")
            
            # Crear modelos
            models = create_acciones_1000_models(db)
            
            if not models:
                logger.error("❌ Error al crear modelos de acciones 1000")
                return False
            
            # Crear todas las tablas
            db.create_all()
            
            logger.info("Tablas creadas exitosamente")
            
            # Verificar que las tablas existen
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            expected_tables = ['actividades_1000', 'fotos_actividades_1000']
            
            for table in expected_tables:
                if table in existing_tables:
                    logger.info(f"Tabla {table} existe")
                else:
                    logger.warning(f"Tabla {table} no encontrada")
            
            # Crear directorio de uploads si no existe
            upload_dir = os.path.join(app.static_folder, 'uploads', 'acciones_1000')
            os.makedirs(upload_dir, exist_ok=True)
            logger.info(f"Directorio de uploads creado: {upload_dir}")
            
            logger.info("Base de datos de 1000 Acciones en 1 Día inicializada correctamente")
            return True
            
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {str(e)}")
        return False

def verify_database_connection():
    """Verificar conexión a la base de datos"""
    
    try:
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Intentar una consulta simple
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                result.close()
            
            logger.info("Conexión a la base de datos exitosa")
            return True
            
    except Exception as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        return False

def show_database_info():
    """Mostrar información de la base de datos"""
    
    try:
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Obtener información de las tablas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            logger.info("Información de la base de datos:")
            logger.info(f"   - Total de tablas: {len(tables)}")
            
            for table in tables:
                if 'acciones_1000' in table or 'fotos_actividades_1000' in table:
                    columns = inspector.get_columns(table)
                    logger.info(f"   - Tabla {table}: {len(columns)} columnas")
                    
                    for column in columns:
                        logger.info(f"     * {column['name']}: {column['type']}")
            
            return True
            
    except Exception as e:
        logger.error(f"Error al obtener información de la base de datos: {str(e)}")
        return False

def main():
    """Función principal"""
    
    logger.info("Iniciando script de inicialización de base de datos para 1000 Acciones en 1 Día")
    
    # Verificar conexión
    if not verify_database_connection():
        logger.error("No se puede continuar sin conexión a la base de datos")
        sys.exit(1)
    
    # Inicializar base de datos
    if init_acciones_1000_database():
        logger.info("Inicialización completada exitosamente")
        
        # Mostrar información
        show_database_info()
        
        logger.info("La aplicación está lista para usar")
    else:
        logger.error("Error en la inicialización")
        sys.exit(1)

if __name__ == "__main__":
    main()
