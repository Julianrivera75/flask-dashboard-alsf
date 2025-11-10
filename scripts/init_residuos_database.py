"""
Script para inicializar la base de datos de acciones de residuos
Crea las tablas necesarias y verifica la conexión
"""
import logging
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models.acciones_residuos import AccionResiduos
from models.user import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def init_residuos_database():
    """Inicializar base de datos de acciones de residuos"""
    
    app = create_app()
    
    # Configurar la base de datos de residuos
    with app.app_context():
        # La configuración ya está hecha en app_modular.py
        # Solo necesitamos crear las tablas
        
        logging.info("Inicializando base de datos de acciones de residuos...")
        residuos_db_uri = app.config.get('RESIDUOS_DATABASE_URI', 'sqlite:///residuos.db')
        logging.info(f"URI de base de datos: {residuos_db_uri[:50]}...")
        
        # Crear todas las tablas si no existen
        try:
            # Flask-SQLAlchemy detecta automáticamente el __bind_key__ del modelo
            # y crea las tablas en la base de datos correcta
            db.create_all()
            logging.info("Tablas de acciones de residuos creadas/verificadas")
            
            # Verificar que la tabla existe y está accesible
            try:
                count = AccionResiduos.query.count()
                logging.info(f"Registros actuales en la base de datos: {count}")
            except Exception as query_error:
                logging.warning(f"No se pudo consultar registros (puede ser normal si la tabla esta vacia): {query_error}")
            
            logging.info("Base de datos de acciones de residuos inicializada exitosamente!")
            return True
            
        except Exception as e:
            logging.error(f"Error creando tablas de acciones de residuos: {e}")
            import traceback
            logging.error(traceback.format_exc())
            return False


if __name__ == '__main__':
    success = init_residuos_database()
    sys.exit(0 if success else 1)

