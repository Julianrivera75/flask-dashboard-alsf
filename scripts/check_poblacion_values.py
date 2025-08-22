#!/usr/bin/env python3
"""
Script para verificar los valores exactos de la columna "Población impactada" 
en la hoja de San Bernardo
"""

import requests
import csv
from io import StringIO

def check_poblacion_values():
    # URL de la hoja de San Bernardo
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU/gviz/tq?tqx=out:csv"
    
    try:
        print("🔍 Conectando a Google Sheets...")
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        
        # Procesar CSV
        csv_text = response.text
        csv_io = StringIO(csv_text)
        reader = csv.DictReader(csv_io)
        
        # Encontrar la columna correcta
        headers = reader.fieldnames
        print(f"📋 Headers encontrados: {headers}")
        
        # Buscar la columna de población impactada
        poblacion_col = None
        for header in headers:
            if 'Población impactada' in header:
                poblacion_col = header
                break
        
        if not poblacion_col:
            print("❌ No se encontró la columna 'Población impactada'")
            return
        
        print(f"✅ Columna encontrada: '{poblacion_col}'")
        print(f"📏 Longitud del nombre: {len(poblacion_col)} caracteres")
        print(f"🔍 Caracteres ASCII: {[ord(c) for c in poblacion_col]}")
        
        # Leer todos los valores
        valores = []
        total = 0
        fila_num = 1
        
        for row in reader:
            fila_num += 1
            valor = row.get(poblacion_col, '')
            valores.append(valor)
            
            # Intentar convertir a número
            try:
                if valor and valor.strip():
                    # Manejar valores con comas como separadores decimales
                    valor_limpio = valor.replace(',', '.')
                    num_valor = float(valor_limpio)
                    total += num_valor
                    print(f"Fila {fila_num}: '{valor}' -> {num_valor}")
                else:
                    print(f"Fila {fila_num}: '{valor}' -> vacío/0")
            except ValueError:
                print(f"Fila {fila_num}: '{valor}' -> NO es número")
        
        print(f"\n📊 RESUMEN:")
        print(f"📊 Total de filas procesadas: {len(valores)}")
        print(f"📊 Suma total de población impactada: {total:,.0f}")
        print(f"📊 Valores únicos encontrados: {set(valores)}")
        
        # Verificar si hay espacios al final
        espacios_final = [v for v in valores if v and v.endswith(' ')]
        if espacios_final:
            print(f"⚠️ Valores con espacios al final: {espacios_final}")
        
        # Mostrar valores más grandes
        valores_numericos = []
        for v in valores:
            if v and v.strip():
                try:
                    valor_limpio = v.replace(',', '.')
                    valores_numericos.append(float(valor_limpio))
                except:
                    pass
        
        if valores_numericos:
            valores_numericos.sort(reverse=True)
            print(f"🔝 Top 10 valores más grandes: {valores_numericos[:10]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_poblacion_values()
