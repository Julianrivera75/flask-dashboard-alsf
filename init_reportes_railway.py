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
            
            # Crear todos los modelos
            create_models(db)
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ Tablas de reportes creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Tablas creadas: {len(tables)}")
            for table in tables:
                print(f"   - {table}")
            
            # Crear usuario administrador por defecto para reportes
            from models.user import User
            from werkzeug.security import generate_password_hash
            
            admin_user = User.query.filter_by(username='admin_reportes').first()
            if not admin_user:
                admin_user = User(
                    username='admin_reportes',
                    email='admin.reportes@alsf.gov.co',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuario administrador de reportes creado (admin_reportes/admin123)")
            else:
                print("ℹ️  Usuario administrador de reportes ya existe")
            
            # Crear algunos datos de ejemplo para tipos de actividad
            from models.reporte import TipoActividad
            
            tipos_ejemplo = [
                {'nombre': 'Patrullaje', 'descripcion': 'Actividades de patrullaje y vigilancia'},
                {'nombre': 'Operativo', 'descripcion': 'Operativos de seguridad y convivencia'},
                {'nombre': 'Sensibilización', 'descripcion': 'Actividades de sensibilización comunitaria'},
                {'nombre': 'Intervención', 'descripcion': 'Intervenciones en puntos críticos'},
                {'nombre': 'Requisas', 'descripcion': 'Actividades de requisa y decomiso'},
                {'nombre': 'Levantamiento', 'descripcion': 'Levantamiento de cambuches'},
                {'nombre': 'Sellamiento', 'descripcion': 'Sellamiento de establecimientos'},
                {'nombre': 'Acompañamiento', 'descripcion': 'Acompañamiento jurídico y social'}
            ]
            
            for tipo_data in tipos_ejemplo:
                tipo_existente = TipoActividad.query.filter_by(nombre=tipo_data['nombre']).first()
                if not tipo_existente:
                    tipo = TipoActividad(
                        nombre=tipo_data['nombre'],
                        descripcion=tipo_data['descripcion']
                    )
                    db.session.add(tipo)
            
            db.session.commit()
            print("✅ Tipos de actividad de ejemplo creados")
            
            # Crear algunos sectores de ejemplo
            from models.reporte import Sector
            
            sectores_ejemplo = [
                {'nombre': 'Centro', 'descripcion': 'Sector centro de Santa Fe'},
                {'nombre': 'Norte', 'descripcion': 'Sector norte de Santa Fe'},
                {'nombre': 'Sur', 'descripcion': 'Sector sur de Santa Fe'},
                {'nombre': 'Oriente', 'descripcion': 'Sector oriente de Santa Fe'},
                {'nombre': 'Occidente', 'descripcion': 'Sector occidente de Santa Fe'}
            ]
            
            for sector_data in sectores_ejemplo:
                sector_existente = Sector.query.filter_by(nombre=sector_data['nombre']).first()
                if not sector_existente:
                    sector = Sector(
                        nombre=sector_data['nombre'],
                        descripcion=sector_data['descripcion']
                    )
                    db.session.add(sector)
            
            db.session.commit()
            print("✅ Sectores de ejemplo creados")
            
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
