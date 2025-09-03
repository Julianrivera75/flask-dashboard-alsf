#!/usr/bin/env python3
"""
Script para inicializar datos básicos en Railway
Se ejecuta automáticamente al acceder al formulario de reportes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from models import (
    db, User, Reporte, Responsable, TipoActividad,
    Entidad, Sector, ResultadoReporte, ArchivoReporte
)
from datetime import datetime
import logging

def init_railway_data():
    """Inicializar datos básicos en Railway"""
    
    app = create_app()
    with app.app_context():
        logging.info("🚀 Inicializando datos básicos en Railway...")
        
        # Crear todas las tablas si no existen
        try:
            db.create_all()
            logging.info("✅ Tablas creadas/verificadas")
        except Exception as e:
            logging.error(f"❌ Error creando tablas: {e}")
            return False
        
        # Verificar si ya hay datos
        if Responsable.query.first():
            logging.info("⚠️ La base de datos ya tiene datos. Saltando inserción...")
            return True
        
        logging.info("📝 Insertando datos iniciales...")
        
        try:
            # 1. INSERTAR RESPONSABLES (Personal ALSF)
            responsables = [
                "ANDERSON TORRES SALCEDO",
                "ANGIE LORENA RAIRAN CARREÑO",
                "CAMILO ANDRES ALVAREZ MARQUEZ",
                "CARLOS FABIAN RAMIREZ",
                "DIEGO ARMANDO ORTIZ PINEDA",
                "FRANCISCO JAVIER DIAZ CANASTEROS",
                "HERNAN ALONSO NOVOA HERRERA",
                "IVAN RAMIRO MARTINEZ GUZMAN",
                "JOHANNA IBET GARAY ALVAREZ",
                "JOSE DAVID RODRIGUEZ REYES",
                "KAROL VANESA CASTIBLANCO NOHAVA",
                "MANUEL EDBERTO MARTINEZ MOSQUERA",
                "OLGA LUCIA MARTINEZ MOLINA",
                "PEDRO IGNACIO BELTRAN QUINTERO",
                "SARA INES TAVERA OCHOA",
                "YESSICA PAOLA OLIVEROS YATE",
                "ANYELA GINETH PEDRAZA HERNANDEZ",
                "BRAYAN DAVID PAEZ ACHURY",
                "CARLOS ANTONIO ROMERO DUARTE",
                "DAIZ ARGEL SOLANO",
                "ELKIN JOSE SIERRA BRACHO",
                "GUSTAVO ALBERTO DE LA ROSA FLOREZ",
                "INGRID IVONE MORALES BERNAL",
                "JAVIER ORLANDO DIAZ PULIDO",
                "JONATHAN CAMILO SUAREZ BULA",
                "JOSE GIOVANNY QUINTERO RINCON",
                "LEIDY CAROLINA MORA CHAPARRO",
                "MARIA CAMILA RUEDA PULIDO",
                "OSCAR RENE ORTIZ RODRIGUEZ",
                "ROBERT MAURICIO VARGAS BAUTISTA",
                "YEISON DAVID CORREA ARIAS",
                "ANGELICA MILENA IBAÑEZ PIRAQUIVE",
                "BRYAN JOSEPH CASTILLO ACEVEDO",
                "CARLOS ARTURO ROA DIAZ",
                "DANERY ALEXANDRA HENAO DELGADO",
                "FENNER ANDRES VARGAS RODRIGUEZ",
                "HERMAN YESID MUEGUES TOVAR",
                "IOSIF DAVID ORTIZ RODRIGUEZ",
                "JEAN PAUL PERILLA GARZON",
                "JONNATHAN ALEJANDRO PATARROYO FIGUEROA",
                "KAREN MICHEL MAHECHA ESPINOSA",
                "LUIS ANTONIO CELIS CASTELLANOS",
                "MILENA FAIZURE TORRES HERNANDEZ",
                "PAOLA ANDREA CARDOZO SANCHEZ",
                "SANTIAGO FELIPE GUTIERREZ MERIÑO",
                "YENY ANDREA GARZON MENDOZA"
            ]
            
            for nombre in responsables:
                responsable = Responsable(nombre=nombre, activo=True)
                db.session.add(responsable)
            
            logging.info(f"✅ {len(responsables)} responsables insertados")
            
            # 2. INSERTAR TIPOS DE ACTIVIDAD
            tipos_actividad = [
                "ESTRATEGIA SAN VICTORINO",
                "SOSTENIMIENTO Y MONITOREO ESPACIO PÚBLICO CARRERA SÉPTIMA",
                "SOSTENIMIENTO Y MONITOREO ESPACIO PÚBLICO SAN BERNARDO",
                "SOSTENIMIENTO Y MONITOREO ESPACIO PÚBLICO SAN VICTORINO",
                "MONITOREO, SEGUIMIENTO Y ACOMPAÑAMIENTO PARQUE NACIONAL COMUNIDAD INDIGENA",
                "REUNIÓN INSTITUCIONAL",
                "REUNIÓN CON COMUNIDAD",
                "REUNIÓN DE EQUIPO",
                "RECUPERACIÓN, SEGUIMIENTO Y/O SOSTENIMIENTO ESPACIO PÚBLICO",
                "ACOMPAÑAMIENTO ENTORNOS ESCOLARES",
                "CAMPAÑAS DE PREVENCIÓN Y/O SENSIBILIZACION",
                "OPERATIVO IVC",
                "OPERATIVO CONTROL A PERSONAS",
                "DESMONTE CAMBUCHES",
                "MONITOREO DRON",
                "APOYO ADMINISTRATIVO",
                "ATENCIÓN A VENDEDORES INFORMALES - CARNETIZACIÓN",
                "CONMEMORACION, CELEBRACIÓN O FESTIVAL CON COMUNIDAD",
                "EMBELLECIMIENTO Y/O RESIGNIFICACION",
                "RECORRIDO RECONOCIMIENTO O ACOMPAÑAMIENTO",
                "Otro"
            ]
            
            for nombre in tipos_actividad:
                tipo = TipoActividad(nombre=nombre, activo=True)
                db.session.add(tipo)
            
            logging.info(f"✅ {len(tipos_actividad)} tipos de actividad insertados")
            
            # 3. INSERTAR ENTIDADES
            entidades = [
                "ALSF",
                "MEBOG",
                "IPES",
                "DADEP",
                "UAESP",
                "PROMOAMBIENTAL",
                "INTEGRACIÓN SOCIAL",
                "IDIPRON",
                "MIGRACIÓN COLOMBIA",
                "IDARTES",
                "SECRETARÍA DISTRITAL DE SEGURIDAD",
                "SECRETARÍA DISTRITAL DE SALUD",
                "SECRETARÍA DISTRITAL DE MOVILIDAD",
                "OTRA"
            ]
            
            for nombre in entidades:
                entidad = Entidad(nombre=nombre, activo=True)
                db.session.add(entidad)
            
            logging.info(f"✅ {len(entidades)} entidades insertadas")
            
            # 4. INSERTAR SECTORES
            sectores = [
                "Centro Histórico",
                "Chapinero",
                "Santa Fe",
                "San Cristóbal",
                "Usaquén",
                "Suba",
                "Barrios Unidos",
                "Teusaquillo",
                "Los Mártires",
                "Antonio Nariño",
                "Puente Aranda",
                "La Candelaria",
                "Rafael Uribe Uribe",
                "Ciudad Bolívar",
                "Sumapaz",
                "Usme",
                "Tunjuelito",
                "Bosa",
                "Kennedy",
                "Fontibón",
                "Engativá",
                "Otra"
            ]
            
            for i, nombre in enumerate(sectores):
                sector = Sector(nombre=nombre, orden=i+1, activo=True)
                db.session.add(sector)
            
            logging.info(f"✅ {len(sectores)} sectores insertados")
            
            # 5. CREAR USUARIO ADMIN si no existe
            if not User.query.filter_by(email='admin@alsf.gov.co').first():
                admin_user = User(
                    email='admin@alsf.gov.co',
                    password='ALSF2025',
                    first_name='Administrador',
                    last_name='ALSF',
                    role='admin'
                )
                db.session.add(admin_user)
                logging.info("✅ Usuario admin creado")
            
            # Confirmar cambios
            db.session.commit()
            logging.info("🎉 Datos básicos inicializados exitosamente en Railway!")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Error inicializando datos: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🚀 INICIALIZANDO DATOS BÁSICOS EN RAILWAY")
    print("=" * 50)
    
    success = init_railway_data()
    
    if success:
        print("\n🎯 ¡DATOS INICIALIZADOS EXITOSAMENTE!")
        print("Ahora las opciones del formulario deberían aparecer en Railway")
    else:
        print("\n❌ Error al inicializar datos")
        sys.exit(1)
