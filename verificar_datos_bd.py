#!/usr/bin/env python3
"""
Script para verificar exactamente qué datos están en la base de datos
"""

import requests
import json
from datetime import datetime

def verificar_datos_bd():
    """Verifica exactamente qué datos están en la base de datos"""
    base_url = "http://localhost:5000"
    
    print("🔍 VERIFICACIÓN DETALLADA DE DATOS EN BD")
    print("=" * 60)
    
    # 1. Verificar responsables
    print("\n1️⃣ RESPONSABLES:")
    try:
        response = requests.get(f"{base_url}/api/responsables")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total: {len(data)} responsables")
            for resp in data:
                print(f"   - ID: {resp.get('id')} | Nombre: {resp.get('nombre')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar tipos de actividad
    print("\n2️⃣ TIPOS DE ACTIVIDAD:")
    try:
        response = requests.get(f"{base_url}/api/tipos-actividad")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total: {len(data)} tipos")
            for tipo in data:
                print(f"   - ID: {tipo.get('id')} | Nombre: {tipo.get('nombre')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Verificar entidades
    print("\n3️⃣ ENTIDADES:")
    try:
        response = requests.get(f"{base_url}/api/entidades")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total: {len(data)} entidades")
            for ent in data:
                print(f"   - ID: {ent.get('id')} | Nombre: {ent.get('nombre')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Verificar reportes
    print("\n4️⃣ REPORTES:")
    try:
        response = requests.get(f"{base_url}/api/reportes")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"   Total: {len(data)} reportes")
                if data:
                    print("   Primeros 3 reportes:")
                    for i, reporte in enumerate(data[:3]):
                        print(f"     Reporte {i+1}: ID={reporte.get('id')}, Fecha={reporte.get('fecha_reporte')}, Coordenadas=({reporte.get('latitud')}, {reporte.get('longitud')})")
            elif isinstance(data, dict) and 'reportes' in data:
                reportes = data['reportes']
                print(f"   Total: {len(reportes)} reportes")
                if reportes:
                    print("   Primeros 3 reportes:")
                    for i, reporte in enumerate(reportes[:3]):
                        print(f"     Reporte {i+1}: ID={reporte.get('id')}, Fecha={reporte.get('fecha_reporte')}, Coordenadas=({reporte.get('latitud')}, {reporte.get('longitud')})")
            else:
                print(f"   Formato inesperado: {type(data)}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Verificar estado de la BD
    print("\n5️⃣ ESTADO DE LA BASE DE DATOS:")
    try:
        response = requests.get(f"{base_url}/init-db")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estado: {data.get('message')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Verificación completada")

if __name__ == "__main__":
    verificar_datos_bd()
