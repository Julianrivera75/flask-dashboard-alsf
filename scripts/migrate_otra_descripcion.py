#!/usr/bin/env python3
"""
Script de migración para cambiar el campo otra_descripcion de VARCHAR(200) a TEXT
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def migrate_otra_descripcion():
    """Migrar el campo otra_descripcion de VARCHAR(200) a TEXT"""
    
    # Obtener la URL de la base de datos
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('REPORTES_DATABASE_URL')
    
    if not database_url:
        print("❌ Error: No se encontró DATABASE_URL o REPORTES_DATABASE_URL en las variables de entorno")
        return False
    
    try:
        # Crear conexión a la base de datos
        engine = create_engine(database_url)
        
        print("🔄 Iniciando migración del campo otra_descripcion...")
        
        # Verificar si la tabla existe
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'resultados_reporte'
                );
            """))
            
            table_exists = result.scalar()
            
            if not table_exists:
                print("❌ Error: La tabla 'resultados_reporte' no existe")
                return False
            
            # Verificar el tipo actual del campo
            result = conn.execute(text("""
                SELECT data_type, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'resultados_reporte' 
                AND column_name = 'otra_descripcion';
            """))
            
            column_info = result.fetchone()
            
            if not column_info:
                print("❌ Error: El campo 'otra_descripcion' no existe en la tabla")
                return False
            
            current_type, max_length = column_info
            print(f"📋 Tipo actual del campo: {current_type}({max_length})")
            
            # Si ya es TEXT, no hacer nada
            if current_type == 'text':
                print("✅ El campo ya es de tipo TEXT, no se requiere migración")
                return True
            
            # Realizar la migración
            print("🔄 Cambiando el tipo de campo de VARCHAR(200) a TEXT...")
            
            conn.execute(text("""
                ALTER TABLE resultados_reporte 
                ALTER COLUMN otra_descripcion TYPE TEXT;
            """))
            
            conn.commit()
            
            print("✅ Migración completada exitosamente")
            print("📋 El campo 'otra_descripcion' ahora acepta textos de cualquier longitud")
            
            return True
            
    except SQLAlchemyError as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Script de migración - Campo otra_descripcion")
    print("=" * 50)
    
    success = migrate_otra_descripcion()
    
    if success:
        print("\n✅ Migración completada exitosamente")
        print("💡 Ahora puedes guardar reportes con descripciones largas")
    else:
        print("\n❌ La migración falló")
        print("💡 Revisa los errores anteriores y vuelve a intentar")
        sys.exit(1)

if __name__ == "__main__":
    main()
