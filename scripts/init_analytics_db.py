#!/usr/bin/env python3
"""
Script para inicializar las tablas de analytics en la base de datos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models.analytics import Base
from models import db

def init_analytics_tables():
    """Inicializar las tablas de analytics"""
    try:
        app = create_app()
        
        with app.app_context():
            print("🔧 Inicializando tablas de analytics...")
            
            # Crear todas las tablas de analytics
            Base.metadata.create_all(bind=db.engine)
            
            print("✅ Tablas de analytics creadas exitosamente")
            
            # Verificar que las tablas existan
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            analytics_tables = ['page_views', 'user_events', 'traffic_summary']
            
            for table in analytics_tables:
                if table in tables:
                    print(f"✅ Tabla {table} existe")
                else:
                    print(f"❌ Tabla {table} no encontrada")
            
            print("\n🎯 Sistema de analytics listo para usar!")
            print("📊 Accede a /analytics/dashboard para ver las métricas")
            
    except Exception as e:
        print(f"❌ Error inicializando analytics: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_analytics_tables()
