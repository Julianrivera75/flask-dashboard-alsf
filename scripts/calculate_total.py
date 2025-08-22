#!/usr/bin/env python3
"""
Script simple para calcular el total de la columna "Población impactada"
"""

import requests
import csv
from io import StringIO

def calculate_total():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1v4duGwbae0AAHPAEXsGZPZqWI35JkgHyhHg4yHTIpPU/gviz/tq?tqx=out:csv"
    
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        
        csv_io = StringIO(response.text)
        reader = csv.DictReader(csv_io)
        
        # Buscar la columna
        poblacion_col = None
        for header in reader.fieldnames:
            if 'Población impactada' in header:
                poblacion_col = header
                break
        
        if not poblacion_col:
            print("❌ Columna no encontrada")
            return
        
        print(f"✅ Columna: '{poblacion_col}'")
        
        # Calcular total
        total = 0
        fila = 1
        
        for row in reader:
            fila += 1
            valor = row.get(poblacion_col, '')
            
            if valor and valor.strip():
                try:
                    valor_limpio = valor.replace(',', '.')
                    num_valor = float(valor_limpio)
                    total += num_valor
                except:
                    print(f"❌ Fila {fila}: '{valor}' no es número")
        
        print(f"📊 Total calculado: {total:,.0f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    calculate_total()
