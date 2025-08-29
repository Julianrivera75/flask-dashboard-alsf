#!/usr/bin/env python3
"""
Script para verificar la estructura de directorios de uploads
"""

import os
import sys

def verificar_uploads():
    """Verificar la estructura de directorios de uploads"""
    
    print("🔍 VERIFICANDO ESTRUCTURA DE UPLOADS")
    print("=" * 50)
    
    # Obtener directorio raíz del proyecto
    proyecto_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Directorio raíz del proyecto: {proyecto_root}")
    
    # Verificar directorio static/uploads
    static_uploads = os.path.join(proyecto_root, 'static', 'uploads')
    print(f"Directorio static/uploads: {static_uploads}")
    
    if os.path.exists(static_uploads):
        print("✅ static/uploads existe")
        
        # Verificar subdirectorios
        for item in os.listdir(static_uploads):
            item_path = os.path.join(static_uploads, item)
            if os.path.isdir(item_path):
                print(f"📁 Subdirectorio: {item}")
                # Contar archivos en el subdirectorio
                archivos = [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]
                print(f"   📄 Archivos: {len(archivos)}")
                if archivos:
                    print(f"   📄 Ejemplos: {archivos[:3]}")
            else:
                print(f"📄 Archivo: {item}")
    else:
        print("❌ static/uploads NO existe")
        # Crear el directorio
        try:
            os.makedirs(static_uploads, exist_ok=True)
            print("✅ static/uploads creado")
        except Exception as e:
            print(f"❌ Error creando static/uploads: {e}")
    
    # Verificar directorio acciones_1000
    acciones_1000_dir = os.path.join(static_uploads, 'acciones_1000')
    print(f"\nDirectorio acciones_1000: {acciones_1000_dir}")
    
    if os.path.exists(acciones_1000_dir):
        print("✅ acciones_1000 existe")
        archivos = [f for f in os.listdir(acciones_1000_dir) if os.path.isfile(os.path.join(acciones_1000_dir, f))]
        print(f"📄 Total de fotos: {len(archivos)}")
        if archivos:
            print(f"📄 Ejemplos: {archivos[:5]}")
    else:
        print("❌ acciones_1000 NO existe")
        # Crear el directorio
        try:
            os.makedirs(acciones_1000_dir, exist_ok=True)
            print("✅ acciones_1000 creado")
        except Exception as e:
            print(f"❌ Error creando acciones_1000: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Verificación completada")

if __name__ == "__main__":
    verificar_uploads()

