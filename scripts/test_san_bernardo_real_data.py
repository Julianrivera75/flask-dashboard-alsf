#!/usr/bin/env python3
"""
Script de prueba para verificar que obtenemos los datos correctos de San Bernardo
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.google_sheets_service import GoogleSheetsConnector
from config import Config

def test_san_bernardo_real_data():
    """Prueba la obtención de datos reales de San Bernardo"""
    print("🧪 PRUEBA DE DATOS REALES DE SAN BERNARDO")
    print("=" * 60)
    
    # Crear instancia de configuración
    config = Config()
    
    print(f"📋 Configuración:")
    print(f"   - Sheet ID: {config.SAN_BERNARDO_SHEET_ID}")
    print(f"   - Archivo de credenciales: {config.SAN_BERNARDO_CREDENTIALS_FILE}")
    print()
    
    try:
        # Conectar a Google Sheets
        connector = GoogleSheetsConnector(
            credentials_file=config.SAN_BERNARDO_CREDENTIALS_FILE,
            credentials_env_var=config.SAN_BERNARDO_CREDENTIALS_ENV_VAR
        )
        
        if not connector.connect():
            print("❌ No se pudo conectar a Google Sheets")
            return False
        
        print("✅ Conexión exitosa con Google Sheets")
        
        # Obtener datos en bruto
        raw_data, headers = connector.get_sheet_data(config.SAN_BERNARDO_SHEET_ID)
        
        if not raw_data:
            print("❌ No se pudieron obtener datos")
            return False
        
        print(f"📊 Datos obtenidos: {len(raw_data)} registros")
        print(f"📋 Columnas disponibles: {len(headers)}")
        
        # Mostrar las primeras columnas para verificar la estructura
        print(f"\n🔍 PRIMERAS 10 COLUMNAS:")
        for i, header in enumerate(headers[:10]):
            print(f"   {i+1:2d}. {header}")
        
        if len(headers) > 10:
            print(f"   ... y {len(headers) - 10} columnas más")
        
        # Verificar que tenemos las columnas esperadas
        columnas_esperadas = [
            'Entidad',
            'Población impactada', 
            'Fecha final de ejecución',
            'Descripción de los compromisos',
            'Resultados ( Resumen del resultado obtenido de la intervención)'
        ]
        
        print(f"\n✅ VERIFICACIÓN DE COLUMNAS ESPERADAS:")
        for columna in columnas_esperadas:
            if columna in headers:
                print(f"   ✅ {columna}")
            else:
                print(f"   ❌ {columna} - NO ENCONTRADA")
        
        # Mostrar ejemplo del primer registro
        if raw_data:
            primer_registro = raw_data[0]
            print(f"\n🔍 EJEMPLO DEL PRIMER REGISTRO:")
            print("-" * 50)
            
            for columna in columnas_esperadas:
                if columna in primer_registro:
                    valor = primer_registro[columna]
                    # Truncar valores muy largos
                    if isinstance(valor, str) and len(valor) > 100:
                        valor = valor[:100] + "..."
                    print(f"📋 {columna}: {valor}")
                else:
                    print(f"📋 {columna}: NO DISPONIBLE")
        
        # Contar registros con datos válidos
        registros_con_fecha = 0
        registros_con_poblacion = 0
        registros_con_entidad = 0
        
        for row in raw_data:
            if row.get('Fecha final de ejecución', '').strip():
                registros_con_fecha += 1
            if row.get('Población impactada', '').strip():
                registros_con_poblacion += 1
            if row.get('Entidad', '').strip():
                registros_con_entidad += 1
        
        print(f"\n📊 ESTADÍSTICAS DE DATOS:")
        print(f"   📅 Registros con fecha: {registros_con_fecha}")
        print(f"   👥 Registros con población: {registros_con_poblacion}")
        print(f"   🏢 Registros con entidad: {registros_con_entidad}")
        print(f"   📈 Total de registros: {len(raw_data)}")
        
        # Verificar que tenemos aproximadamente 70 registros como esperabas
        if 60 <= len(raw_data) <= 80:
            print(f"✅ ✅ ✅ PERFECTO: {len(raw_data)} registros (esperado ~70)")
        else:
            print(f"⚠️ ⚠️ ⚠️ ATENCIÓN: {len(raw_data)} registros (esperado ~70)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print(f"🚀 Iniciando prueba de datos reales de San Bernardo - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_san_bernardo_real_data()
    
    if success:
        print("\n🎯 RESULTADO FINAL: ✅ Datos de San Bernardo obtenidos correctamente")
        print("   Ahora deberías ver las gráficas con los datos reales de San Bernardo")
        return 0
    else:
        print("\n❌ RESULTADO FINAL: Falló la obtención de datos")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
