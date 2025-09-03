#!/usr/bin/env python3
"""
Script para crear usuario administrador por defecto
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models import db, User

def create_admin_user():
    """Crear usuario administrador por defecto"""
    
    app = create_app()
    
    with app.app_context():
        # Verificar si el usuario admin ya existe
        existing_admin = User.query.filter_by(email='admin@alsf.gov.co').first()
        
        if existing_admin:
            print("✅ Usuario administrador ya existe: admin@alsf.gov.co")
            return True
        
        try:
            # Crear usuario administrador
            admin_user = User(
                email='admin@alsf.gov.co',
                password='ALSF2025',
                first_name='Administrador',
                last_name='ALSF',
                role='admin'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente:")
            print("   Email: admin@alsf.gov.co")
            print("   Contraseña: ALSF2025")
            print("   Rol: admin")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear usuario administrador: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("👨‍💼 CREANDO USUARIO ADMINISTRADOR")
    print("=" * 40)
    
    success = create_admin_user()
    
    if success:
        print("\n🎯 ¡LISTO!")
        print("Ahora puede acceder al sistema con:")
        print("Email: admin@alsf.gov.co")
        print("Contraseña: ALSF2025")
    else:
        print("\n❌ Error al crear usuario administrador")
        sys.exit(1)
