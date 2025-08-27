#!/usr/bin/env python3
"""
Script para configurar exactamente qué opciones debe tener la base de datos
"""

import requests
import json

def configurar_opciones_personalizadas():
    """Configura las opciones exactas que debe tener la base de datos"""
    base_url = "http://localhost:5000"
    
    print("🔧 CONFIGURACIÓN DE OPCIONES PERSONALIZADAS")
    print("=" * 60)
    print("Este script te permitirá especificar exactamente qué opciones")
    print("debe tener tu base de datos, eliminando las opciones por defecto.")
    print()
    
    # OPCIONES PERSONALIZADAS - MODIFICA ESTAS LISTAS SEGÚN LO QUE TENÍAS EN LOCAL
    print("📋 CONFIGURACIÓN ACTUAL:")
    print("(Modifica estas listas en el código según lo que tenías en local)")
    print()
    
    # 1. RESPONSABLES PERSONALIZADOS
    responsables_personalizados = [
        # AGREGA AQUÍ SOLO LOS RESPONSABLES QUE TENÍAS EN LOCAL
        # Ejemplo:
        # "Alcaldía Local Santa Fe",
        # "Secretaría de Gobierno",
        # etc.
    ]
    
    # 2. TIPOS DE ACTIVIDAD PERSONALIZADOS
    tipos_actividad_personalizados = [
        # AGREGA AQUÍ SOLO LOS TIPOS QUE TENÍAS EN LOCAL
        # Ejemplo:
        # "Operativo de Seguridad",
        # "Jornada de Salud",
        # etc.
    ]
    
    # 3. ENTIDADES PERSONALIZADAS
    entidades_personalizadas = [
        # AGREGA AQUÍ SOLO LAS ENTIDADES QUE TENÍAS EN LOCAL
        # Ejemplo:
        # "Alcaldía Mayor de Bogotá",
        # "Policía Nacional",
        # etc.
    ]
    
    # 4. SECTORES PERSONALIZADOS
    sectores_personalizados = [
        # AGREGA AQUÍ SOLO LOS SECTORES QUE TENÍAS EN LOCAL
        # Ejemplo:
        # "Sector 1",
        # "Sector 2",
        # etc.
    ]
    
    print("1️⃣ RESPONSABLES PERSONALIZADOS:")
    if responsables_personalizados:
        for resp in responsables_personalizados:
            print(f"   - {resp}")
    else:
        print("   ⚠️ Lista vacía - Agrega los responsables que tenías en local")
    
    print("\n2️⃣ TIPOS DE ACTIVIDAD PERSONALIZADOS:")
    if tipos_actividad_personalizados:
        for tipo in tipos_actividad_personalizados:
            print(f"   - {tipo}")
    else:
        print("   ⚠️ Lista vacía - Agrega los tipos que tenías en local")
    
    print("\n3️⃣ ENTIDADES PERSONALIZADAS:")
    if entidades_personalizadas:
        for ent in entidades_personalizadas:
            print(f"   - {ent}")
    else:
        print("   ⚠️ Lista vacía - Agrega las entidades que tenías en local")
    
    print("\n4️⃣ SECTORES PERSONALIZADOS:")
    if sectores_personalizados:
        for sec in sectores_personalizados:
            print(f"   - {sec}")
    else:
        print("   ⚠️ Lista vacía - Agrega los sectores que tenías en local")
    
    print("\n" + "=" * 60)
    print("📝 INSTRUCCIONES:")
    print("1. Modifica las listas en este script")
    print("2. Agrega SOLO las opciones que tenías en local")
    print("3. Ejecuta el script nuevamente")
    print("4. Las opciones por defecto se eliminarán automáticamente")
    
    return {
        'responsables': responsables_personalizados,
        'tipos_actividad': tipos_actividad_personalizados,
        'entidades': entidades_personalizadas,
        'sectores': sectores_personalizados
    }

if __name__ == "__main__":
    configurar_opciones_personalizadas()
