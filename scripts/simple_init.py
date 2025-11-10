#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models import db

def init_database():
    app = create_app()
    with app.app_context():
        print("🔧 Inicializando base de datos...")
        
        # Eliminar todas las tablas existentes
        db.drop_all()
        print("🗑️ Tablas existentes eliminadas")
        
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        print("🎉 Base de datos inicializada exitosamente!")

if __name__ == '__main__':
    init_database()
















