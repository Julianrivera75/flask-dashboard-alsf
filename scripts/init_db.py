#!/usr/bin/env python3
"""
Script para inicializar la base de datos
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

def init_database():
    app = create_app()
    with app.app_context():
        print("🔧 Inicializando base de datos...")
        
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        # Verificar si ya hay datos
        if Responsable.query.first():
            print("⚠️ La base de datos ya tiene datos. Saltando inserción...")
            return
        
        print("📝 Insertando datos iniciales...")
        
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
        
        for i, nombre in enumerate(responsables):
            responsable = Responsable(nombre=nombre)
            db.session.add(responsable)
        
        print(f"✅ {len(responsables)} responsables insertados")
        
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
        
        for i, nombre in enumerate(tipos_actividad):
            tipo = TipoActividad(nombre=nombre)
            db.session.add(tipo)
        
        print(f"✅ {len(tipos_actividad)} tipos de actividad insertados")
        

        
        # 4. INSERTAR ENTIDADES
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
        
        for i, nombre in enumerate(entidades):
            entidad = Entidad(nombre=nombre)
            db.session.add(entidad)
        
        print(f"✅ {len(entidades)} entidades insertadas")
        
        # 5. INSERTAR SECTORES (ejemplo básico para Bogotá)
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
            sector = Sector(nombre=nombre, orden=i+1)
            db.session.add(sector)
        
        print(f"✅ {len(sectores)} sectores insertados")
        
        # 6. CREAR USUARIO ADMIN
        from werkzeug.security import generate_password_hash
        admin_user = User(
            email='admin@alsf.gov.co',
            password='ALSF2025',
            first_name='Administrador',
            last_name='ALSF',
            role='admin'
        )
        db.session.add(admin_user)
        print("✅ Usuario admin creado")
        
        # Confirmar cambios
        db.session.commit()
        print("🎉 Base de datos inicializada exitosamente!")
        print(f"📊 Total de registros:")
        print(f"   - Responsables: {Responsable.query.count()}")
        print(f"   - Tipos de actividad: {TipoActividad.query.count()}")
        print(f"   - Entidades: {Entidad.query.count()}")
        print(f"   - Sectores: {Sector.query.count()}")
        print(f"   - Usuarios: {User.query.count()}")

if __name__ == '__main__':
    init_database()
