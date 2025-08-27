#!/usr/bin/env python3
"""
Script para diagnosticar el estado de los reportes en la base de datos
"""

import requests
import json
from datetime import datetime

def diagnosticar_reportes():
    """Diagnostica el estado de los reportes"""
    base_url = "http://localhost:5000"
    
    print("🔍 DIAGNÓSTICO DE REPORTES")
    print("=" * 50)
    
    # 1. Verificar si la API está funcionando
    print("\n1️⃣ Verificando API de reportes...")
    try:
        response = requests.get(f"{base_url}/api/reportes")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando - Status: {response.status_code}")
            print(f"📊 Total de reportes: {len(data)}")
            
            if data:
                print("\n📋 Primeros 3 reportes:")
                for i, reporte in enumerate(data[:3]):
                    print(f"   Reporte {i+1}:")
                    print(f"     ID: {reporte.get('id')}")
                    print(f"     Fecha: {reporte.get('fecha_reporte')}")
                    print(f"     Coordenadas: {reporte.get('latitud')}, {reporte.get('longitud')}")
                    print(f"     Tipo Actividad: {reporte.get('tipo_actividad_id')}")
                    print(f"     Responsable: {reporte.get('responsable_id')}")
        else:
            print(f"❌ API error - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al conectar con API: {e}")
    
    # 2. Verificar tipos de actividad
    print("\n2️⃣ Verificando tipos de actividad...")
    try:
        response = requests.get(f"{base_url}/api/tipos-actividad")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tipos de actividad: {len(data)} encontrados")
            for tipo in data:
                print(f"   - {tipo.get('id')}: {tipo.get('nombre')}")
        else:
            print(f"❌ Error en tipos de actividad: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al obtener tipos de actividad: {e}")
    
    # 3. Verificar responsables
    print("\n3️⃣ Verificando responsables...")
    try:
        response = requests.get(f"{base_url}/api/responsables")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Responsables: {len(data)} encontrados")
            for resp in data:
                print(f"   - {resp.get('id')}: {resp.get('nombre')}")
        else:
            print(f"❌ Error en responsables: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al obtener responsables: {e}")
    
    # 4. Verificar entidades
    print("\n4️⃣ Verificando entidades...")
    try:
        response = requests.get(f"{base_url}/api/entidades")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Entidades: {len(data)} encontradas")
            for ent in data:
                print(f"   - {ent.get('id')}: {ent.get('nombre')}")
        else:
            print(f"❌ Error en entidades: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al obtener entidades: {e}")
    
    # 5. Verificar estado de la base de datos
    print("\n5️⃣ Verificando estado de la base de datos...")
    try:
        response = requests.get(f"{base_url}/init-db")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado BD: {data.get('message')}")
        else:
            print(f"❌ Error al verificar BD: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al verificar BD: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Diagnóstico completado")

if __name__ == "__main__":
    diagnosticar_reportes()
