#!/usr/bin/env python3
"""
Script para inicializar la base de datos de reportes ALSF
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

def init_reportes_database():
    """Inicializar base de datos de reportes ALSF"""
    
    app = create_app()
    with app.app_context():
        logging.info("🚀 Inicializando base de datos de reportes ALSF...")
        
        # Crear todas las tablas si no existen
        try:
            db.create_all()
            logging.info("✅ Tablas de reportes creadas/verificadas")
        except Exception as e:
            logging.error(f"❌ Error creando tablas de reportes: {e}")
            return False
        
        # Verificar si ya hay datos
        if Responsable.query.first():
            logging.info("⚠️ La base de datos de reportes ya tiene datos. Saltando inserción...")
            return True
        
        logging.info("📝 Insertando datos iniciales para reportes...")
        
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
            logging.info("🎉 Base de datos de reportes ALSF inicializada exitosamente!")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Error inicializando base de datos de reportes: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🚀 INICIALIZANDO BASE DE DATOS DE REPORTES ALSF")
    print("=" * 50)
    
    success = init_reportes_database()
    
    if success:
        print("\n🎯 ¡BASE DE DATOS DE REPORTES INICIALIZADA!")
        print("Ahora el formulario de reportes tendrá todas las opciones disponibles")
    else:
        print("\n❌ Error al inicializar base de datos de reportes")
        sys.exit(1)





