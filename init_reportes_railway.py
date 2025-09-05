#!/usr/bin/env python3
"""
Script de inicialización específico para la base de datos de reportes en Railway
Configura solo las tablas necesarias para "Santa Fe Camina Segura: Reportes de Seguridad y Convivencia"
"""

import os
import sys
from flask import Flask
from config import ProductionConfig

def init_reportes_database():
    """
    Inicializa la base de datos de reportes de Railway
    """
    print("🚀 Inicializando base de datos de REPORTES en Railway...")
    print("=" * 60)
    
    # Verificar variables de entorno
    reportes_db_url = os.environ.get('REPORTES_DATABASE_URL')
    if not reportes_db_url:
        print("❌ Error: No se encontró REPORTES_DATABASE_URL en las variables de entorno")
        print("   Asegúrate de que Railway esté configurado con una segunda base de datos PostgreSQL")
        return False
    
    print("✅ REPORTES_DATABASE_URL encontrada")
    print(f"   Host: {reportes_db_url.split('@')[1].split('/')[0] if '@' in reportes_db_url else 'N/A'}")
    
    try:
        # Crear aplicación Flask con configuración de producción
        app = Flask(__name__)
        app.config.from_object(ProductionConfig)
        
        # Importar modelos después de configurar la app
        from models import db, create_models
        
        # Inicializar base de datos
        db.init_app(app)
        
        with app.app_context():
            print("📋 Creando tablas de REPORTES en Railway...")
            
            # Solo crear las tablas (los modelos ya están definidos)
            db.create_all()
            
            print("✅ Tablas de reportes creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Tablas creadas: {len(tables)}")
            for table in tables:
                print(f"   - {table}")
            
            # Las tablas están listas, no necesitamos crear datos de ejemplo
            print("ℹ️  Las tablas están listas para recibir datos")
            
            print("\n🎉 Inicialización de base de datos de REPORTES completada exitosamente!")
            print("📋 Esta base de datos es específica para 'Santa Fe Camina Segura: Reportes de Seguridad y Convivencia'")
            return True
            
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_reportes_database()
    sys.exit(0 if success else 1)
