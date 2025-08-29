from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, FileField, 
    IntegerField, HiddenField
)
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError
from wtforms.widgets import TextArea

class Acciones1000Form(FlaskForm):
    """Formulario para 1000 acciones en 1 día"""
    
    # 1. Nombre del responsable de la actividad (obligatorio)
    nombre_responsable = StringField(
        'Nombre del responsable de la actividad *',
        validators=[DataRequired(message='El nombre del responsable es obligatorio')],
        description='Ingrese el nombre completo del responsable de la actividad'
    )
    
    # 2. Tipo de actividad (obligatorio) - Lista desplegable
    tipo_actividad = SelectField(
        '¿Cuál actividad está reportando? *',
        validators=[DataRequired(message='Debe seleccionar un tipo de actividad')],
        choices=[
            ('', 'Seleccione una actividad'),
            ('Diálogo diferencial LGBTI', 'Diálogo diferencial LGBTI'),
            ('Fiesta Mayor', 'Fiesta Mayor'),
            ('Feria de Emprendedoras y Productoras Locales', 'Feria de Emprendedoras y Productoras Locales'),
            ('Recuperación entornos tramos universitarios - sector las aguas-', 'Recuperación entornos tramos universitarios - sector las aguas-'),
            ('DANZA', 'DANZA'),
            ('Jornada de embellecimiento', 'Jornada de embellecimiento'),
            ('Jornada de Protección y Bienestar Animal - PYBA', 'Jornada de Protección y Bienestar Animal - PYBA'),
            ('MES MAYOR', 'MES MAYOR'),
            ('INAUGURACIÓN CENTRO DE EXPERIENCIA TIC', 'INAUGURACIÓN CENTRO DE EXPERIENCIA TIC'),
            ('Actividad', 'Actividad'),
            ('Encuentro', 'Encuentro'),
            ('Fugate al centro', 'Fugate al centro')
        ],
        description='Seleccione el tipo de actividad que está reportando'
    )
    
    # 3. Área responsable (obligatorio) - Lista desplegable
    area_responsable = SelectField(
        'Área responsable de la actividad *',
        validators=[DataRequired(message='Debe seleccionar un área responsable')],
        choices=[
            ('', 'Seleccione un área'),
            ('Ambiente', 'Ambiente'),
            ('Seguridad', 'Seguridad'),
            ('Deportes', 'Deportes'),
            ('Participación', 'Participación'),
            ('Innovación', 'Innovación'),
            ('Planeación', 'Planeación'),
            ('otro', 'Otro')
        ],
        description='Seleccione el área responsable de la actividad'
    )
    
    # Campo adicional para "otro" área
    area_otro = StringField(
        'Especifique otra área',
        validators=[Optional()],
        description='Si seleccionó "Otro", especifique cuál es el área responsable'
    )
    
    # 4. Número de personas impactadas (obligatorio)
    personas_impactadas = IntegerField(
        'Número de personas impactadas *',
        validators=[
            DataRequired(message='El número de personas impactadas es obligatorio'),
            NumberRange(min=1, message='Debe ser al menos 1 persona')
        ],
        description='Ingrese el número total de personas que fueron impactadas por la actividad'
    )
    
    # 5. Descripción detallada (obligatorio)
    descripcion_detallada = TextAreaField(
        'Descripción detallada de la actividad *',
        validators=[DataRequired(message='La descripción detallada es obligatoria')],
        description='Describa detalladamente qué se realizó en la actividad',
        widget=TextArea(),
        render_kw={"rows": 5, "placeholder": "Describa detalladamente la actividad realizada..."}
    )
    
    # 6. Observaciones adicionales (opcional)
    observaciones_adicionales = TextAreaField(
        'Observaciones adicionales',
        validators=[Optional()],
        description='Información adicional o comentarios sobre la actividad (opcional)',
        widget=TextArea(),
        render_kw={"rows": 3, "placeholder": "Observaciones adicionales (opcional)..."}
    )
    
    # 7. Ubicación en el mapa (obligatorio) - Campos ocultos
    latitud = HiddenField(
        'Latitud',
        validators=[DataRequired(message='Debe seleccionar una ubicación en el mapa')]
    )
    
    longitud = HiddenField(
        'Longitud',
        validators=[DataRequired(message='Debe seleccionar una ubicación en el mapa')]
    )
    
    # 8. Fotos de la actividad (obligatorio)
    fotos = FileField(
        'Adjuntar fotos de la actividad *',
        validators=[DataRequired(message='Debe adjuntar al menos una foto de la actividad')],
        description='Seleccione hasta 4 fotos de la actividad realizada'
    )
    
    def validate_area_otro(self, field):
        """Validar que si se selecciona 'otro', se especifique cuál es"""
        if self.area_responsable.data == 'otro' and not field.data:
            raise ValidationError('Si selecciona "Otro", debe especificar cuál es el área responsable')
    
    def validate_fotos(self, field):
        """Validar que se suban archivos de imagen"""
        if field.data:
            # Verificar que sea un archivo de imagen
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
            filename = field.data.filename
            if filename:
                extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                if extension not in allowed_extensions:
                    raise ValidationError('Solo se permiten archivos de imagen (PNG, JPG, JPEG, GIF, BMP, WEBP)')
    
    def validate_fotos_multiple(self, field):
        """Validar múltiples archivos de imagen"""
        if field.data:
            # Si es una lista de archivos (múltiples)
            if isinstance(field.data, list):
                if len(field.data) > 4:
                    raise ValidationError('Puede seleccionar máximo 4 imágenes')
                
                # Validar cada archivo
                for file in field.data:
                    if file and file.filename:
                        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
                        extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                        if extension not in allowed_extensions:
                            raise ValidationError(f'El archivo {file.filename} no es una imagen válida')
                        
                        # Validar tamaño (5MB máximo)
                        if file.content_length and file.content_length > 5 * 1024 * 1024:
                            raise ValidationError(f'El archivo {file.filename} excede el tamaño máximo de 5MB')
