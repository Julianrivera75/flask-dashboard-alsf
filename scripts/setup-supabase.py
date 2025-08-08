#!/usr/bin/env python3
"""
Script para configurar Supabase para ALSF
Autor: ALSF Team
Fecha: 2024
"""

import os
import requests
import json
from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseSetup:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("❌ Variables de entorno SUPABASE_URL y SUPABASE_ANON_KEY requeridas")
            logger.info("💡 Configura las variables de entorno:")
            logger.info("   SUPABASE_URL=https://tu-proyecto.supabase.co")
            logger.info("   SUPABASE_ANON_KEY=tu-anon-key")
            return
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def create_table_reportes(self) -> bool:
        """Crear tabla de reportes"""
        try:
            logger.info("🗄️ Creando tabla de reportes...")
            
            # SQL para crear la tabla
            sql = """
            CREATE TABLE IF NOT EXISTS reportes (
                id BIGSERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                telefono VARCHAR(50),
                organizacion VARCHAR(255),
                direccion TEXT NOT NULL,
                latitud DECIMAL(10, 8) NOT NULL,
                longitud DECIMAL(11, 8) NOT NULL,
                tipo_reporte VARCHAR(100) NOT NULL,
                descripcion TEXT NOT NULL,
                prioridad VARCHAR(50) DEFAULT 'media',
                fecha_reporte DATE,
                hora_reporte TIME,
                fotos_urls TEXT[],
                timestamp TIMESTAMP DEFAULT NOW(),
                user_agent TEXT,
                estado VARCHAR(50) DEFAULT 'pendiente',
                fecha_actualizacion TIMESTAMP,
                
                CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
                CONSTRAINT valid_coordinates CHECK (
                    latitud BETWEEN -90 AND 90 AND 
                    longitud BETWEEN -180 AND 180
                )
            );
            
            -- Crear índices
            CREATE INDEX IF NOT EXISTS idx_reportes_tipo ON reportes(tipo_reporte);
            CREATE INDEX IF NOT EXISTS idx_reportes_estado ON reportes(estado);
            CREATE INDEX IF NOT EXISTS idx_reportes_fecha ON reportes(fecha_reporte);
            CREATE INDEX IF NOT EXISTS idx_reportes_coords ON reportes(latitud, longitud);
            CREATE INDEX IF NOT EXISTS idx_reportes_timestamp ON reportes(timestamp DESC);
            """
            
            # Ejecutar SQL usando la API REST
            url = f"{self.supabase_url}/rest/v1/rpc/exec_sql"
            response = requests.post(url, headers=self.headers, json={'sql': sql})
            
            if response.status_code == 200:
                logger.info("✅ Tabla de reportes creada exitosamente")
                return True
            else:
                logger.error(f"❌ Error creando tabla: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en create_table_reportes: {e}")
            return False
    
    def insert_test_data(self) -> bool:
        """Insertar datos de prueba"""
        try:
            logger.info("🧪 Insertando datos de prueba...")
            
            test_data = {
                'nombre': 'Juan Pérez',
                'email': 'juan@example.com',
                'telefono': '3001234567',
                'organizacion': 'Comunidad Local',
                'direccion': 'Calle 123, Bogotá',
                'latitud': 4.7110,
                'longitud': -74.0721,
                'tipo_reporte': 'infraestructura',
                'descripcion': 'Bache en la calle principal que necesita reparación urgente',
                'prioridad': 'alta',
                'fecha_reporte': '2024-01-15',
                'hora_reporte': '14:30:00',
                'estado': 'pendiente'
            }
            
            url = f"{self.supabase_url}/rest/v1/reportes"
            response = requests.post(url, headers=self.headers, json=test_data)
            
            if response.status_code == 201:
                logger.info("✅ Datos de prueba insertados exitosamente")
                return True
            else:
                logger.error(f"❌ Error insertando datos: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en insert_test_data: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Probar conexión a Supabase"""
        try:
            logger.info("🔗 Probando conexión a Supabase...")
            
            url = f"{self.supabase_url}/rest/v1/reportes?select=count"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("✅ Conexión a Supabase exitosa")
                return True
            else:
                logger.error(f"❌ Error de conexión: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en test_connection: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas básicas"""
        try:
            logger.info("📊 Obteniendo estadísticas...")
            
            url = f"{self.supabase_url}/rest/v1/reportes"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                reports = response.json()
                
                stats = {
                    'total_reportes': len(reports),
                    'por_tipo': {},
                    'por_prioridad': {},
                    'por_estado': {}
                }
                
                for report in reports:
                    # Contar por tipo
                    tipo = report.get('tipo_reporte', 'otro')
                    stats['por_tipo'][tipo] = stats['por_tipo'].get(tipo, 0) + 1
                    
                    # Contar por prioridad
                    prioridad = report.get('prioridad', 'media')
                    stats['por_prioridad'][prioridad] = stats['por_prioridad'].get(prioridad, 0) + 1
                    
                    # Contar por estado
                    estado = report.get('estado', 'pendiente')
                    stats['por_estado'][estado] = stats['por_estado'].get(estado, 0) + 1
                
                logger.info(f"✅ Estadísticas obtenidas: {stats['total_reportes']} reportes")
                return stats
            else:
                logger.error(f"❌ Error obteniendo estadísticas: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error en get_statistics: {e}")
            return {}
    
    def setup_complete(self) -> bool:
        """Configuración completa de Supabase"""
        logger.info("🚀 Iniciando configuración completa de Supabase...")
        
        # 1. Probar conexión
        if not self.test_connection():
            return False
        
        # 2. Crear tabla
        if not self.create_table_reportes():
            return False
        
        # 3. Insertar datos de prueba
        if not self.insert_test_data():
            return False
        
        # 4. Obtener estadísticas
        stats = self.get_statistics()
        
        logger.info("🎉 Configuración de Supabase completada exitosamente!")
        logger.info(f"📊 Total de reportes: {stats.get('total_reportes', 0)}")
        
        return True

def main():
    """Función principal"""
    print("🚀 Configurando Supabase para ALSF")
    print("=" * 50)
    
    setup = SupabaseSetup()
    
    if setup.supabase_url and setup.supabase_key:
        success = setup.setup_complete()
        
        if success:
            print("\n✅ Configuración completada exitosamente!")
            print("\n📋 Próximos pasos:")
            print("1. Actualizar variables de entorno en tu app Flask")
            print("2. Probar el formulario georeferenciado")
            print("3. Configurar almacenamiento para fotos")
            print("4. Implementar tiempo real")
        else:
            print("\n❌ Error en la configuración")
            print("Verifica las variables de entorno y la conexión")
    else:
        print("\n❌ Variables de entorno no configuradas")
        print("Configura SUPABASE_URL y SUPABASE_ANON_KEY")

if __name__ == "__main__":
    main() 