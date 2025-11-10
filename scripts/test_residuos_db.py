"""
Script de prueba para verificar la base de datos de acciones de residuos
"""
import sys
import os
from datetime import date, datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models.acciones_residuos import AccionResiduos, LOCALIDADES_VALIDAS
from models.user import db

def test_residuos_database():
    """Probar la base de datos de residuos"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("PRUEBA DE BASE DE DATOS DE ACCIONES DE RESIDUOS")
        print("=" * 60)
        
        # 1. Verificar que la tabla existe
        print("\n1. Verificando que la tabla existe...")
        try:
            count = AccionResiduos.query.count()
            print(f"   [OK] Tabla existe. Registros actuales: {count}")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
            return False
        
        # 2. Listar localidades válidas
        print("\n2. Localidades validas:")
        for i, localidad in enumerate(LOCALIDADES_VALIDAS, 1):
            print(f"   {i:2d}. {localidad}")
        
        # 3. Crear un registro de prueba
        print("\n3. Creando registro de prueba...")
        try:
            registro_prueba = AccionResiduos(
                localidad='Santa Fe',
                numero_operativos=5,
                numero_comparendos=10,
                numero_sensibilizaciones=3,
                fecha_operacion=date.today(),
                usuario_registro='test_user',
                observaciones='Registro de prueba'
            )
            
            # Validar localidad
            if not AccionResiduos.validar_localidad(registro_prueba.localidad):
                print(f"   [ERROR] Localidad '{registro_prueba.localidad}' no es valida")
                return False
            
            db.session.add(registro_prueba)
            db.session.commit()
            print(f"   [OK] Registro creado con ID: {registro_prueba.id}")
            
        except Exception as e:
            print(f"   [ERROR] Error creando registro: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        
        # 4. Consultar el registro
        print("\n4. Consultando registro creado...")
        try:
            registro = AccionResiduos.query.filter_by(id=registro_prueba.id).first()
            if registro:
                print(f"   [OK] Registro encontrado:")
                print(f"      - Localidad: {registro.localidad}")
                print(f"      - Operativos: {registro.numero_operativos}")
                print(f"      - Comparendos: {registro.numero_comparendos}")
                print(f"      - Sensibilizaciones: {registro.numero_sensibilizaciones}")
                print(f"      - Fecha operacion: {registro.fecha_operacion}")
            else:
                print("   [ERROR] Registro no encontrado")
                return False
        except Exception as e:
            print(f"   [ERROR] Error consultando registro: {e}")
            return False
        
        # 5. Probar método to_dict
        print("\n5. Probando metodo to_dict()...")
        try:
            dict_registro = registro.to_dict()
            print(f"   [OK] Conversion a diccionario exitosa")
            print(f"      Keys: {list(dict_registro.keys())}")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
            return False
        
        # 6. Eliminar registro de prueba
        print("\n6. Eliminando registro de prueba...")
        try:
            db.session.delete(registro)
            db.session.commit()
            print("   [OK] Registro eliminado")
        except Exception as e:
            print(f"   [ERROR] Error eliminando registro: {e}")
            db.session.rollback()
            return False
        
        # 7. Verificar configuración de bind
        print("\n7. Verificando configuracion de bind...")
        try:
            bind_key = AccionResiduos.__bind_key__
            print(f"   [OK] Bind key configurado: '{bind_key}'")
            
            # Verificar que el bind está en la configuración
            binds = app.config.get('SQLALCHEMY_BINDS', {})
            if 'residuos' in binds:
                print(f"   [OK] Bind 'residuos' configurado en app")
                print(f"      URI: {binds['residuos'][:50]}...")
            else:
                print("   [WARNING] Bind 'residuos' no encontrado en configuracion")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
        
        print("\n" + "=" * 60)
        print("[OK] TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        return True


if __name__ == '__main__':
    success = test_residuos_database()
    sys.exit(0 if success else 1)

