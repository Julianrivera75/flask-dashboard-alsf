#!/usr/bin/env python3
"""
Script para limpiar todos los registros de la base de datos de Railway
Elimina actividades, fotos y analytics para dejar la BD en blanco
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def limpiar_railway_database():
    """Limpiar todos los registros de la base de datos de Railway"""
    
    print("🧹 LIMPIANDO BASE DE DATOS DE RAILWAY")
    print("=" * 50)
    
    # Obtener la URL de la base de datos desde variables de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Variable DATABASE_URL no encontrada")
        print("Configura esta variable en tu entorno local:")
        print("set DATABASE_URL=${{ acciones-1000-db.DATABASE_URL }}")
        return False
    
    try:
        # Crear conexión a la base de datos
        print("🔌 Conectando a PostgreSQL...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
        
        # Limpiar registros de fotos primero (por las foreign keys)
        print("\n📸 Limpiando registros de fotos...")
        with engine.connect() as connection:
            # Contar fotos antes de eliminar
            count_fotos = connection.execute(text("SELECT COUNT(*) FROM fotos_actividades_1000")).scalar()
            print(f"   📊 Fotos encontradas: {count_fotos}")
            
            if count_fotos > 0:
                connection.execute(text("DELETE FROM fotos_actividades_1000"))
                print("   ✅ Registros de fotos eliminados")
            else:
                print("   ℹ️  No hay fotos para eliminar")
        
        # Limpiar registros de actividades
        print("\n📋 Limpiando registros de actividades...")
        with engine.connect() as connection:
            # Contar actividades antes de eliminar
            count_actividades = connection.execute(text("SELECT COUNT(*) FROM actividades_1000")).scalar()
            print(f"   📊 Actividades encontradas: {count_actividades}")
            
            if count_actividades > 0:
                connection.execute(text("DELETE FROM actividades_1000"))
                print("   ✅ Registros de actividades eliminados")
            else:
                print("   ℹ️  No hay actividades para eliminar")
        
        # Limpiar registros de analytics (page_views)
        print("\n📊 Limpiando registros de analytics...")
        with engine.connect() as connection:
            # Contar page_views antes de eliminar
            count_page_views = connection.execute(text("SELECT COUNT(*) FROM page_views")).scalar()
            print(f"   📊 Registros de analytics encontrados: {count_page_views}")
            
            if count_page_views > 0:
                connection.execute(text("DELETE FROM page_views"))
                print("   ✅ Registros de analytics eliminados")
            else:
                print("   ℹ️  No hay registros de analytics para eliminar")
        
        # Reiniciar secuencias de auto-incremento
        print("\n🔄 Reiniciando secuencias de auto-incremento...")
        with engine.connect() as connection:
            # Reiniciar secuencia de actividades_1000
            connection.execute(text("ALTER SEQUENCE actividades_1000_id_seq RESTART WITH 1"))
            print("   ✅ Secuencia de actividades reiniciada")
            
            # Reiniciar secuencia de fotos_actividades_1000
            connection.execute(text("ALTER SEQUENCE fotos_actividades_1000_id_seq RESTART WITH 1"))
            print("   ✅ Secuencia de fotos reiniciada")
            
            # Reiniciar secuencia de page_views
            connection.execute(text("ALTER SEQUENCE page_views_id_seq RESTART WITH 1"))
            print("   ✅ Secuencia de analytics reiniciada")
        
        # Verificar estado final
        print("\n🔍 Verificando estado final...")
        with engine.connect() as connection:
            count_fotos_final = connection.execute(text("SELECT COUNT(*) FROM fotos_actividades_1000")).scalar()
            count_actividades_final = connection.execute(text("SELECT COUNT(*) FROM actividades_1000")).scalar()
            count_page_views_final = connection.execute(text("SELECT COUNT(*) FROM page_views")).scalar()
            
            print(f"   📊 Fotos restantes: {count_fotos_final}")
            print(f"   📊 Actividades restantes: {count_actividades_final}")
            print(f"   📊 Analytics restantes: {count_page_views_final}")
        
        print("\n🎉 ¡BASE DE DATOS LIMPIADA EXITOSAMENTE!")
        print("✅ Todos los registros eliminados")
        print("✅ Secuencias reiniciadas")
        print("✅ Base de datos lista para uso en producción")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO LIMPIEZA DE BASE DE DATOS")
    print("=" * 50)
    
    success = limpiar_railway_database()
    
    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. La base de datos está completamente limpia")
        print("2. Puedes probar el formulario nuevamente")
        print("3. Los indicadores mostrarán 0/32 y 0 personas impactadas")
        print("4. El mapa estará vacío, listo para nuevas actividades")
    else:
        print("\n❌ La limpieza falló")
        print("Revisa los errores y vuelve a intentar")
        sys.exit(1)
