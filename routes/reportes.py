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
        # Obtener todas las opciones para los dropdowns
        responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
        tipos_actividad = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
        entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
        
        return render_template('reportes/formulario.html',
                             responsables=responsables,
                             tipos_actividad=tipos_actividad,
                             entidades=entidades)
    except Exception as e:
        logging.error(f"Error en formulario_reporte: {e}")
        flash('Error al cargar el formulario', 'error')
        return redirect(url_for('index'))

@reportes_bp.route('/api/responsables')
@login_required
def api_responsables():
    """API para obtener responsables"""
    try:
        responsables = Responsable.query.filter_by(activo=True).order_by(Responsable.nombre).all()
        return jsonify([{'id': r.id, 'nombre': r.nombre} for r in responsables])
    except Exception as e:
        logging.error(f"Error en api_responsables: {e}")
        return jsonify({'error': 'Error al obtener responsables'}), 500

@reportes_bp.route('/api/tipos-actividad')
@login_required
def api_tipos_actividad():
    """API para obtener tipos de actividad"""
    try:
        tipos = TipoActividad.query.filter_by(activo=True).order_by(TipoActividad.nombre).all()
        return jsonify([{'id': t.id, 'nombre': t.nombre} for t in tipos])
    except Exception as e:
        logging.error(f"Error en api_tipos_actividad: {e}")
        return jsonify({'error': 'Error al obtener tipos de actividad'}), 500



@reportes_bp.route('/api/entidades')
@login_required
def api_entidades():
    """API para obtener entidades"""
    try:
        entidades = Entidad.query.filter_by(activo=True).order_by(Entidad.nombre).all()
        return jsonify([{'id': e.id, 'nombre': e.nombre} for e in entidades])
    except Exception as e:
        logging.error(f"Error en api_entidades: {e}")
        return jsonify({'error': 'Error al obtener entidades'}), 500

@reportes_bp.route('/api/guardar-reporte', methods=['POST'])
@login_required
def api_guardar_reporte():
    """API para guardar un nuevo reporte"""
    try:
        # Obtener datos del formulario
        data = request.get_json()
        
        # Crear el reporte
        reporte = Reporte(
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
            reporte_dict = {
                'id': reporte.id,
                'fecha_reporte': reporte.fecha_reporte.isoformat() if reporte.fecha_reporte else None,
                'responsable': reporte.responsable.nombre if reporte.responsable else None,
                'tipo_actividad': reporte.tipo_actividad.nombre if reporte.tipo_actividad else None,
    
                'latitud': reporte.latitud,
                'longitud': reporte.longitud,
                'estado': reporte.estado
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
