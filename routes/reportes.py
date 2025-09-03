from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import db, Reporte, Responsable, TipoActividad, Entidad, Sector, ResultadoReporte, ArchivoReporte, User
from services.file_service import FileService
from forms.reporte_form import ReporteForm
import logging
from functools import wraps

reportes_bp = Blueprint('reportes', __name__)
file_service = FileService()

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@reportes_bp.route('/formulario-reporte')
@login_required
def formulario_reporte():
    """Muestra el formulario de reporte"""
    try:
        # Verificar si la base de datos está inicializada
        from models import Responsable, TipoActividad, Entidad, Sector
        from app_modular import db
        
        # Intentar crear las tablas si no existen
        try:
            db.create_all()
        except Exception as db_error:
            logging.warning(f"Error al crear tablas: {db_error}")
        
        # Verificar si hay datos básicos y agregar solo los que falten
        logging.info("Verificando y completando datos básicos...")
        
        # 1. RESPONSABLES - Solo agregar los que falten
        responsables_existentes = {r.nombre.lower() for r in Responsable.query.all()}
        responsables_basicos = [
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
        
        for nombre in responsables_basicos:
            if nombre.lower() not in responsables_existentes:
                responsable = Responsable(nombre=nombre, activo=True)
                db.session.add(responsable)
                logging.info(f"Agregado responsable: {nombre}")
        
        # 2. TIPOS DE ACTIVIDAD - Solo agregar los que falten
        tipos_existentes = {t.nombre.lower() for t in TipoActividad.query.all()}
        tipos_basicos = [
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
        
        for nombre in tipos_basicos:
            if nombre.lower() not in tipos_existentes:
                tipo = TipoActividad(nombre=nombre, activo=True)
                db.session.add(tipo)
                logging.info(f"Agregado tipo de actividad: {nombre}")
        
        # 3. ENTIDADES - Solo agregar las que falten
        entidades_existentes = {e.nombre.lower() for e in Entidad.query.all()}
        entidades_basicas = [
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
        
        for nombre in entidades_basicas:
            if nombre.lower() not in entidades_existentes:
                entidad = Entidad(nombre=nombre, activo=True)
                db.session.add(entidad)
                logging.info(f"Agregada entidad: {nombre}")
        
        # 4. SECTORES - Solo agregar los que falten
        sectores_existentes = {s.nombre.lower() for s in Sector.query.all()}
        sectores_basicos = [
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
        
        for nombre in sectores_basicos:
            if nombre.lower() not in sectores_existentes:
                sector = Sector(nombre=nombre, activo=True)
                db.session.add(sector)
                logging.info(f"Agregado sector: {nombre}")
        
        # Hacer commit solo si se agregaron nuevos datos
        try:
            db.session.commit()
            logging.info("✅ Base de datos verificada y completada correctamente")
            logging.info(f"📊 Datos cargados: {len(responsables_basicos)} responsables, {len(tipos_basicos)} tipos, {len(entidades_basicas)} entidades, {len(sectores_basicos)} sectores")
        except Exception as commit_error:
            logging.error(f"❌ Error al hacer commit: {commit_error}")
            db.session.rollback()
            # Continuar con datos existentes si falla el commit
        
        # Obtener todas las opciones para los dropdowns
        try:
            responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
            tipos_actividad = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
            entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
            
            logging.info(f"✅ Datos cargados: {len(responsables)} responsables, {len(tipos_actividad)} tipos, {len(entidades)} entidades")
            
        except Exception as e:
            logging.error(f"❌ Error al cargar datos: {e}")
            # Fallback: usar datos básicos si la BD falla
            responsables = []
            tipos_actividad = []
            entidades = []
            
            # Crear opciones básicas como fallback
            try:
                # Crear al menos un responsable básico
                if not Responsable.query.first():
                    responsable = Responsable(nombre="Responsable General", activo=True)
                    db.session.add(responsable)
                
                # Crear al menos un tipo de actividad básico
                if not TipoActividad.query.first():
                    tipo = TipoActividad(nombre="Actividad General", activo=True)
                    db.session.add(tipo)
                
                # Crear al menos una entidad básica
                if not Entidad.query.first():
                    entidad = Entidad(nombre="Entidad General", activo=True)
                    db.session.add(entidad)
                
                db.session.commit()
                
                # Recargar datos después del fallback
                responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
                tipos_actividad = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
                entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
                
                logging.info(f"✅ Fallback creado: {len(responsables)} responsables, {len(tipos_actividad)} tipos, {len(entidades)} entidades")
                
            except Exception as fallback_error:
                logging.error(f"❌ Error en fallback: {fallback_error}")
        
        return render_template('reportes/formulario.html',
                             responsables=responsables,
                             tipos_actividad=tipos_actividad,
                             entidades=entidades)
    except Exception as e:
        logging.error(f"Error en formulario_reporte: {e}")
        flash('Error al cargar el formulario. Inicializando base de datos...', 'warning')
        # Intentar inicializar la base de datos automáticamente
        try:
            from app_modular import init_database
            init_database()
            flash('Base de datos inicializada. Intenta nuevamente.', 'success')
        except Exception as init_error:
            logging.error(f"Error al inicializar automáticamente: {init_error}")
            flash('Error al inicializar la base de datos automáticamente.', 'error')
        
        return redirect(url_for('index'))

@reportes_bp.route('/api/responsables')
@login_required
def api_responsables():
    """API para obtener responsables"""
    try:
        responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
        
        if not responsables:
            logging.warning("⚠️ No hay responsables en la BD, creando fallback...")
            # Crear fallback si no hay datos
            try:
                responsable = Responsable(nombre="Responsable General", activo=True)
                db.session.add(responsable)
                db.session.commit()
                responsables = [responsable]
                logging.info("✅ Fallback de responsable creado")
            except Exception as fallback_error:
                logging.error(f"❌ Error creando fallback: {fallback_error}")
                # Devolver opción básica
                return jsonify([{'id': 1, 'nombre': 'Responsable General'}])
        
        logging.info(f"✅ API responsables: {len(responsables)} encontrados")
        return jsonify([{'id': r.id, 'nombre': r.nombre} for r in responsables])
        
    except Exception as e:
        logging.error(f"❌ Error en api_responsables: {e}")
        # Devolver opción básica en caso de error
        return jsonify([{'id': 1, 'nombre': 'Responsable General'}])

@reportes_bp.route('/api/tipos-actividad')
@login_required
def api_tipos_actividad():
    """API para obtener tipos de actividad"""
    try:
        tipos = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
        
        if not tipos:
            logging.warning("⚠️ No hay tipos de actividad en la BD, creando fallback...")
            # Crear fallback si no hay datos
            try:
                tipo = TipoActividad(nombre="Actividad General", activo=True)
                db.session.add(tipo)
                db.session.commit()
                tipos = [tipo]
                logging.info("✅ Fallback de tipo de actividad creado")
            except Exception as fallback_error:
                logging.error(f"❌ Error creando fallback: {fallback_error}")
                # Devolver opción básica
                return jsonify([{'id': 1, 'nombre': 'Actividad General'}])
        
        logging.info(f"✅ API tipos de actividad: {len(tipos)} encontrados")
        return jsonify([{'id': t.id, 'nombre': t.nombre} for t in tipos])
        
    except Exception as e:
        logging.error(f"❌ Error en api_tipos_actividad: {e}")
        # Devolver opción básica en caso de error
        return jsonify([{'id': 1, 'nombre': 'Actividad General'}])



@reportes_bp.route('/api/entidades')
@login_required
def api_entidades():
    """API para obtener entidades"""
    try:
        entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
        
        if not entidades:
            logging.warning("⚠️ No hay entidades en la BD, creando fallback...")
            # Crear fallback si no hay datos
            try:
                entidad = Entidad(nombre="Entidad General", activo=True)
                db.session.add(entidad)
                db.session.commit()
                entidades = [entidad]
                logging.info("✅ Fallback de entidad creado")
            except Exception as fallback_error:
                logging.error(f"❌ Error creando fallback: {fallback_error}")
                # Devolver opción básica
                return jsonify([{'id': 1, 'nombre': 'Entidad General'}])
        
        logging.info(f"✅ API entidades: {len(entidades)} encontradas")
        return jsonify([{'id': e.id, 'nombre': e.nombre} for e in entidades])
        
    except Exception as e:
        logging.error(f"❌ Error en api_entidades: {e}")
        # Devolver opción básica en caso de error
        return jsonify([{'id': 1, 'nombre': 'Entidad General'}])

@reportes_bp.route('/api/guardar-reporte', methods=['POST'])
@login_required
def api_guardar_reporte():
    """API para guardar un nuevo reporte"""
    try:
        # Obtener datos del formulario
        data = request.get_json()
        
        # Crear el reporte con fecha explícita
        from datetime import datetime
        reporte = Reporte(
            fecha_reporte=datetime.now(),  # Fecha actual explícita
            responsable_id=int(data['responsable_id']),
            latitud=float(data['latitud']),
            longitud=float(data['longitud']),
            tipo_actividad_id=int(data['tipo_actividad_id']),
            acompanamiento_juridico=data.get('acompanamiento_juridico') == 'true',
            observaciones=data.get('observaciones', ''),
            usuario_id=1  # Por ahora hardcodeado, después se puede obtener del usuario logueado
        )
        
        # Determinar sector automáticamente (por ahora se puede hacer manual o con lógica de geolocalización)
        # Por defecto asignar el primer sector
        primer_sector = Sector.query.first()
        if primer_sector:
            reporte.sector_id = primer_sector.id
        
        db.session.add(reporte)
        db.session.flush()  # Para obtener el ID del reporte
        
        # Agregar participantes
        participantes_ids = data.get('participantes_ids', [])
        if isinstance(participantes_ids, str):
            participantes_ids = [participantes_ids]
        for participante_id in participantes_ids:
            participante = Responsable.query.get(int(participante_id))
            if participante:
                reporte.participantes.append(participante)
        
        # Agregar entidades
        entidades_ids = data.get('entidades_ids', [])
        if isinstance(entidades_ids, str):
            entidades_ids = [entidades_ids]
        for entidad_id in entidades_ids:
            entidad = Entidad.query.get(int(entidad_id))
            if entidad:
                reporte.entidades.append(entidad)
        
        # Procesar campos dinámicos
        otro_tipo_actividad = data.get('otro_tipo_actividad', '').strip()
        otra_entidad = data.get('otra_entidad', '').strip()
        
        # Si se seleccionó "Otro" tipo de actividad y se especificó texto
        if str(data['tipo_actividad_id']) == '21' and otro_tipo_actividad:
            # Guardar el texto personalizado en observaciones o crear un campo específico
            if reporte.observaciones:
                reporte.observaciones += f"\n\nTipo de actividad personalizado: {otro_tipo_actividad}"
            else:
                reporte.observaciones = f"Tipo de actividad personalizado: {otro_tipo_actividad}"
        
        # Si se seleccionó "OTRA" entidad y se especificó texto
        if '14' in entidades_ids and otra_entidad:
            if reporte.observaciones:
                reporte.observaciones += f"\n\nEntidad personalizada: {otra_entidad}"
            else:
                reporte.observaciones = f"Entidad personalizada: {otra_entidad}"
        
        # Crear resultados
        resultados = ResultadoReporte(
            reporte_id=reporte.id,
            cambuches_levantados=int(data.get('cambuches_levantados', 0)),
            armas_blancas_decomisadas=int(data.get('armas_blancas_decomisadas', 0)),
            armas_fuego_decomisadas=int(data.get('armas_fuego_decomisadas', 0)),
            requisas=int(data.get('requisas', 0)),
            sellamientos_establecimientos=int(data.get('sellamientos_establecimientos', 0)),
            sensibilizaciones=int(data.get('sensibilizaciones', 0)),
            otra_descripcion=data.get('otra_descripcion', '')
        )
        db.session.add(resultados)
        

        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reporte guardado exitosamente',
            'reporte_id': reporte.id
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error en api_guardar_reporte: {e}")
        return jsonify({'error': f'Error al guardar reporte: {str(e)}'}), 500

@reportes_bp.route('/api/reportes')
@login_required
def api_reportes():
    """API para obtener reportes con filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        categoria_id = request.args.get('categoria_id', type=int)
        estado = request.args.get('estado', '')
        
        query = Reporte.query
        
        if categoria_id:
            query = query.filter_by(tipo_actividad_id=categoria_id)
        if estado:
            query = query.filter_by(estado=estado)
        
        reportes = query.order_by(Reporte.fecha_reporte.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        reportes_data = []
        for reporte in reportes.items:
            # Obtener participantes
            participantes = []
            if reporte.participantes:
                participantes = [{'id': p.id, 'nombre': p.nombre} for p in reporte.participantes]
            
            # Obtener entidades
            entidades = []
            if reporte.entidades:
                entidades = [{'id': e.id, 'nombre': e.nombre} for e in reporte.entidades]
            
            # Obtener resultados
            resultados = []
            if reporte.resultados:
                for resultado in reporte.resultados:
                    resultados.append({
                        'cambuches_levantados': resultado.cambuches_levantados,
                        'armas_blancas_decomisadas': resultado.armas_blancas_decomisadas,
                        'armas_fuego_decomisadas': resultado.armas_fuego_decomisadas,
                        'requisas': resultado.requisas,
                        'sellamientos_establecimientos': resultado.sellamientos_establecimientos,
                        'sensibilizaciones': resultado.sensibilizaciones,
                        'otra_descripcion': resultado.otra_descripcion
                    })
            
            reporte_dict = {
                'id': reporte.id,
                'fecha_reporte': reporte.fecha_reporte.isoformat() if reporte.fecha_reporte else None,
                'responsable': reporte.responsable.nombre if reporte.responsable else None,
                'tipo_actividad': reporte.tipo_actividad.nombre if reporte.tipo_actividad else None,
                'tipo_actividad_id': reporte.tipo_actividad.id if reporte.tipo_actividad else None,
                'acompanamiento_juridico': reporte.acompanamiento_juridico,
                'observaciones': reporte.observaciones,
                'latitud': reporte.latitud,
                'longitud': reporte.longitud,
                'estado': reporte.estado,
                'participantes': participantes,
                'entidades': entidades,
                'resultados': resultados
            }
            reportes_data.append(reporte_dict)
        
        return jsonify({
            'reportes': reportes_data,
            'total': reportes.total,
            'pages': reportes.pages,
            'current_page': page
        })
        
    except Exception as e:
        logging.error(f"Error en api_reportes: {e}")
        return jsonify({'error': 'Error al obtener reportes'}), 500

@reportes_bp.route('/mapa-reportes')
@login_required
def mapa_reportes():
    """Muestra el mapa con todos los reportes"""
    try:
        return render_template('reportes/mapa.html')
    except Exception as e:
        logging.error(f"Error en mapa_reportes: {e}")
        flash('Error al cargar el mapa', 'error')
        return redirect(url_for('index'))
