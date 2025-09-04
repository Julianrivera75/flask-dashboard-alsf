#!/usr/bin/env python3
"""
Script de inicialización para Railway
Configura la base de datos y crea las tablas necesarias
"""

import os
import sys
from flask import Flask
from config import ProductionConfig

def init_railway_database():
    """
    Inicializa la base de datos de Railway
    """
    print("🚀 Inicializando base de datos de Railway...")
    print("=" * 50)
    
    # Verificar variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Error: No se encontró DATABASE_URL en las variables de entorno")
        print("   Asegúrate de que Railway esté configurado con una base de datos PostgreSQL")
        return False
    
    print("✅ DATABASE_URL encontrada")
    print(f"   Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'N/A'}")
    
    try:
        # Crear aplicación Flask con configuración de producción
        app = Flask(__name__)
        app.config.from_object(ProductionConfig)
        
        # Importar modelos después de configurar la app
        from models import db, create_models
        
        # Inicializar base de datos
        db.init_app(app)
        
        with app.app_context():
            print("📋 Creando tablas en Railway...")
            
            # Crear todos los modelos
            create_models(db)
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Tablas creadas: {len(tables)}")
            for table in tables:
                print(f"   - {table}")
            
            # Crear usuario administrador por defecto
            from models.user import User
            from werkzeug.security import generate_password_hash
            
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@alsf.gov.co',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuario administrador creado (admin/admin123)")
            else:
                print("ℹ️  Usuario administrador ya existe")
            
            print("\n🎉 Inicialización de Railway completada exitosamente!")
            return True
            
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_railway_database()
    sys.exit(0 if success else 1)
