#!/usr/bin/env python3
"""
Script para convertir fotos existentes a base64
"""

import os
import sys
import base64
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def convertir_fotos_a_base64():
    """Convertir todas las fotos existentes a base64"""
    
    print("🔄 CONVIRTIENDO FOTOS A BASE64")
    print("=" * 50)
    
    # Obtener DATABASE_URL desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        print("💡 Asegúrate de ejecutar este script en Railway o con DATABASE_URL configurada")
        return False
    
    try:
        # Crear conexión a la base de datos
        print("🔌 Conectando a PostgreSQL...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
        
        # Obtener todas las fotos que no tienen base64
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT id, nombre_archivo, ruta_archivo, tipo_mime 
                FROM fotos_actividades_1000 
                WHERE foto_base64 IS NULL OR foto_base64 = ''
            """))
            fotos_sin_base64 = result.fetchall()
            
            print(f"📸 Fotos sin base64 encontradas: {len(fotos_sin_base64)}")
            
            if not fotos_sin_base64:
                print("✅ Todas las fotos ya tienen base64")
                return True
            
            # Convertir cada foto a base64
            fotos_convertidas = 0
            for foto in fotos_sin_base64:
                foto_id = foto[0]
                nombre_archivo = foto[1]
                ruta_archivo = foto[2]
                tipo_mime = foto[3] or 'image/jpeg'
                
                print(f"🔄 Convirtiendo foto {foto_id}: {nombre_archivo}")
                
                try:
                    # Intentar leer el archivo desde static/uploads
                    # En Railway, esto probablemente fallará, pero lo intentamos
                    file_path = os.path.join('static', ruta_archivo)
                    
                    if os.path.exists(file_path):
                        # Archivo existe localmente
                        with open(file_path, 'rb') as f:
                            foto_bytes = f.read()
                            foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
                        
                        # Actualizar base de datos
                        with engine.connect() as conn:
                            conn.execute(text("""
                                UPDATE fotos_actividades_1000 
                                SET foto_base64 = :foto_base64 
                                WHERE id = :foto_id
                            """), {'foto_base64': foto_base64, 'foto_id': foto_id})
                            conn.commit()
                        
                        fotos_convertidas += 1
                        print(f"✅ Foto {foto_id} convertida a base64")
                        
                    else:
                        # Archivo no existe localmente (caso Railway)
                        print(f"⚠️  Archivo no encontrado: {file_path}")
                        print(f"💡 En Railway, las fotos se pierden al reiniciar")
                        print(f"💡 Esta foto se mostrará como 'No disponible'")
                        
                        # Crear un placeholder base64 (imagen transparente 1x1)
                        placeholder_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
                        
                        # Actualizar base de datos con placeholder
                        with engine.connect() as conn:
                            conn.execute(text("""
                                UPDATE fotos_actividades_1000 
                                SET foto_base64 = :foto_base64 
                                WHERE id = :foto_id
                            """), {'foto_base64': placeholder_base64, 'foto_id': foto_id})
                            conn.commit()
                        
                        fotos_convertidas += 1
                        print(f"✅ Foto {foto_id} marcada como no disponible")
                        
                except Exception as e:
                    print(f"❌ Error convirtiendo foto {foto_id}: {e}")
                    continue
            
            print(f"\n📊 Resumen de conversión:")
            print(f"   Total de fotos procesadas: {len(fotos_sin_base64)}")
            print(f"   Fotos convertidas: {fotos_convertidas}")
            
            # Verificar estado final
            with engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT 
                        COUNT(*) as total_fotos,
                        COUNT(CASE WHEN foto_base64 IS NOT NULL AND foto_base64 != '' THEN 1 END) as con_base64,
                        COUNT(CASE WHEN foto_base64 IS NULL OR foto_base64 = '' THEN 1 END) as sin_base64
                    FROM fotos_actividades_1000
                """))
                stats = result.fetchone()
                
                print(f"\n📈 Estado final de la base de datos:")
                print(f"   Total de fotos: {stats[0]}")
                print(f"   Con base64: {stats[1]}")
                print(f"   Sin base64: {stats[2]}")
        
        print("\n🎉 ¡CONVERSIÓN COMPLETADA!")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🏗️  INICIANDO CONVERSIÓN DE FOTOS A BASE64")
    print("=" * 50)
    
    success = convertir_fotos_a_base64()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Las fotos existentes ahora tienen base64")
        print("2. En Railway se mostrarán como 'No disponible'")
        print("3. Las nuevas fotos se guardarán con base64 completo")
        print("4. Los indicadores deberían funcionar correctamente")
    else:
        print("\n❌ La conversión falló")
        print("Revisa los errores y vuelve a intentar")
        sys.exit(1)
