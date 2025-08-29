#!/usr/bin/env python3
"""
Script para verificar la estructura de directorios de uploads
"""

import os
import sys

def verificar_uploads():
    """Verificar que el directorio de uploads exista y tenga la estructura correcta"""
    print("🔍 VERIFICANDO ESTRUCTURA DE UPLOADS")
    print("=" * 50)
    
    # Obtener la ruta del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Ruta del proyecto: {project_root}")
    
    # Verificar directorio static
    static_dir = os.path.join(project_root, 'static')
    if os.path.exists(static_dir):
        print(f"✅ Directorio static: {static_dir}")
    else:
        print(f"❌ Directorio static NO existe: {static_dir}")
        print("   Creando directorio static...")
        os.makedirs(static_dir, exist_ok=True)
        print("   ✅ Directorio static creado")
    
    # Verificar directorio uploads
    uploads_dir = os.path.join(static_dir, 'uploads')
    if os.path.exists(uploads_dir):
        print(f"✅ Directorio uploads: {uploads_dir}")
    else:
        print(f"❌ Directorio uploads NO existe: {uploads_dir}")
        print("   Creando directorio uploads...")
        os.makedirs(uploads_dir, exist_ok=True)
        print("   ✅ Directorio uploads creado")
    
    # Verificar directorio acciones_1000
    acciones_dir = os.path.join(uploads_dir, 'acciones_1000')
    if os.path.exists(acciones_dir):
        print(f"✅ Directorio acciones_1000: {acciones_dir}")
    else:
        print(f"❌ Directorio acciones_1000 NO existe: {acciones_dir}")
        print("   Creando directorio acciones_1000...")
        os.makedirs(acciones_dir, exist_ok=True)
        print("   ✅ Directorio acciones_1000 creado")
    
    # Verificar permisos de escritura
    try:
        test_file = os.path.join(acciones_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✅ Permisos de escritura: OK")
    except Exception as e:
        print(f"❌ Error de permisos: {e}")
    
    # Listar archivos existentes
    print(f"\n📋 Archivos en acciones_1000:")
    if os.path.exists(acciones_dir):
        files = os.listdir(acciones_dir)
        if files:
            for file in files:
                file_path = os.path.join(acciones_dir, file)
                size = os.path.getsize(file_path)
                print(f"   📄 {file} ({size} bytes)")
        else:
            print("   📭 No hay archivos")
    
    print("\n🎯 ESTRUCTURA VERIFICADA")
    print("=" * 50)

if __name__ == "__main__":
    verificar_uploads()

