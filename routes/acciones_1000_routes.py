from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import pytz
from forms.acciones_1000_form import Acciones1000Form
from models.acciones_1000 import create_acciones_1000_models
from models import db
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Crear blueprint
acciones_1000_bp = Blueprint('acciones_1000', __name__, url_prefix='/acciones-1000')

# Obtener modelos (cacheado)
_models_cache = None

def get_colombia_now():
    """Obtener la hora actual de Colombia"""
    colombia_tz = pytz.timezone('America/Bogota')
    utc_now = datetime.utcnow()
    colombia_time = colombia_tz.fromutc(utc_now)
    return colombia_time

def get_models():
    """Obtener los modelos de acciones 1000 (cacheado)"""
    global _models_cache
    try:
        if _models_cache is None:
            _models_cache = create_acciones_1000_models(db)
        return _models_cache
    except Exception as e:
        logger.error(f"Error al obtener modelos: {e}")
        return None

@acciones_1000_bp.route('/')
def index():
    """Página principal del formulario de 1000 acciones"""
    try:
        form = Acciones1000Form()
        return render_template('acciones_1000/index.html', form=form)
    except Exception as e:
        logger.error(f"Error en página principal de acciones 1000: {e}")
        flash('Error al cargar el formulario', 'error')
        return render_template('error.html', error=str(e)), 500

@acciones_1000_bp.route('/submit', methods=['POST'])
def submit_actividad():
    """Procesar el envío del formulario de actividad"""
    try:
        form = Acciones1000Form()
        
        if not form.validate():
            # Si hay errores de validación, devolver JSON con errores
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0] if field_errors else 'Error de validación'
            
            return jsonify({
                'success': False,
                'errors': errors,
                'message': 'Por favor corrija los errores en el formulario'
            }), 400
        
        # Obtener modelos
        models = get_models()
        if not models:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor'
            }), 500
        
        Actividad1000 = models['Actividad1000']
        FotoActividad1000 = models['FotoActividad1000']
        
        # Crear nueva actividad
        nueva_actividad = Actividad1000(
            nombre_responsable=form.nombre_responsable.data,
            tipo_actividad=form.tipo_actividad.data,
            area_responsable=form.area_responsable.data,
            area_otro=form.area_otro.data if form.area_responsable.data == 'otro' else None,
            personas_impactadas=form.personas_impactadas.data,
            descripcion_detallada=form.descripcion_detallada.data,
            observaciones_adicionales=form.observaciones_adicionales.data,
            latitud=float(form.latitud.data),
            longitud=float(form.longitud.data)
        )
        
        # Guardar actividad en base de datos
        db.session.add(nueva_actividad)
        db.session.flush()  # Para obtener el ID
        
        # Procesar fotos
        fotos = request.files.getlist('fotos')
        
        # Validar límite de fotos
        if len(fotos) > 4:
            return jsonify({
                'success': False,
                'message': 'Puede seleccionar máximo 4 imágenes'
            }), 400
        
        # Validar que haya al menos una foto
        if len(fotos) == 0 or not any(foto.filename for foto in fotos):
            return jsonify({
                'success': False,
                'message': 'Debe seleccionar al menos una imagen'
            }), 400
        
        fotos_procesadas = []
        
        for foto in fotos:
            if foto and foto.filename:
                # Validar tipo de archivo
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
                extension = foto.filename.rsplit('.', 1)[1].lower()
                if extension not in allowed_extensions:
                    return jsonify({
                        'success': False,
                        'message': f'El archivo {foto.filename} no es una imagen válida'
                    }), 400
                
                # Validar tamaño (5MB máximo)
                foto.seek(0, 2)  # Ir al final del archivo
                file_size = foto.tell()
                foto.seek(0)  # Volver al inicio
                
                if file_size > 5 * 1024 * 1024:  # 5MB
                    return jsonify({
                        'success': False,
                        'message': f'El archivo {foto.filename} excede el tamaño máximo de 5MB'
                    }), 400
                
                # Generar nombre único para el archivo
                nombre_archivo = f"{uuid.uuid4().hex}.{extension}"
                
                # Crear directorio si no existe
                upload_dir = os.path.join(current_app.static_folder, 'uploads', 'acciones_1000')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Ruta completa del archivo
                ruta_archivo = os.path.join(upload_dir, nombre_archivo)
                
                # Guardar archivo
                foto.save(ruta_archivo)
                
                # Convertir foto a base64 para almacenamiento persistente
                import base64
                with open(ruta_archivo, 'rb') as f:
                    foto_base64 = base64.b64encode(f.read()).decode('utf-8')
                
                # Crear registro en base de datos con base64
                nueva_foto = FotoActividad1000(
                    actividad_id=nueva_actividad.id,
                    nombre_original=foto.filename,
                    nombre_archivo=nombre_archivo,
                    ruta_archivo=f'uploads/acciones_1000/{nombre_archivo}',
                    tipo_mime=foto.content_type,
                    tamano_bytes=os.path.getsize(ruta_archivo),
                    foto_base64=foto_base64  # Nuevo campo para base64
                )
                
                db.session.add(nueva_foto)
                fotos_procesadas.append(nueva_foto)
        
        # Commit final
        db.session.commit()
        
        logger.info(f"Actividad 1000 creada exitosamente: ID {nueva_actividad.id}")
        
        return jsonify({
            'success': True,
            'message': 'Actividad registrada exitosamente',
            'actividad_id': nueva_actividad.id,
            'fotos_procesadas': len(fotos_procesadas)
        })
        
    except Exception as e:
        logger.error(f"Error al procesar actividad 1000: {e}")
        db.session.rollback()
        
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor al procesar la actividad'
        }), 500

@acciones_1000_bp.route('/listar')
def listar_actividades():
    """Listar todas las actividades registradas"""
    try:
        models = get_models()
        if not models:
            flash('Error al cargar las actividades', 'error')
            return redirect(url_for('acciones_1000.index'))
        
        Actividad1000 = models['Actividad1000']
        
        # Obtener actividades ordenadas por fecha de creación
        actividades = Actividad1000.query.filter_by(estado='activo').order_by(
            Actividad1000.fecha_creacion.desc()
        ).all()
        
        return render_template('acciones_1000/listar.html', actividades=actividades)
        
    except Exception as e:
        logger.error(f"Error al listar actividades: {e}")
        flash('Error al cargar las actividades', 'error')
        return redirect(url_for('acciones_1000.index'))

@acciones_1000_bp.route('/api/actividades')
def api_actividades():
    """API para obtener actividades en formato JSON"""
    try:
        models = get_models()
        if not models:
            return jsonify({'error': 'Error interno del servidor'}), 500
        
        Actividad1000 = models['Actividad1000']
        
        # Obtener actividades activas
        actividades = Actividad1000.query.filter_by(estado='activo').all()
        
        # Convertir a diccionario
        actividades_data = []
        for actividad in actividades:
            actividad_dict = actividad.to_dict()
            # Agregar información de fotos
            actividad_dict['fotos'] = [foto.to_dict() for foto in actividad.fotos]
            actividades_data.append(actividad_dict)
        
        return jsonify({
            'success': True,
            'actividades': actividades_data,
            'total': len(actividades_data)
        })
        
    except Exception as e:
        logger.error(f"Error en API de actividades: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@acciones_1000_bp.route('/mapa')
def mapa_actividades():
    """Página del mapa con todas las actividades"""
    try:
        return render_template('acciones_1000/mapa.html')
    except Exception as e:
        logger.error(f"Error en página del mapa: {e}")
        flash('Error al cargar el mapa', 'error')
        return redirect(url_for('acciones_1000.index'))
