from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, FileField, 
    BooleanField, IntegerField, SelectMultipleField
)
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError

class ReporteForm(FlaskForm):
    """Formulario para crear reportes de actividades ALSF"""
    
    # Responsable (obligatorio) - Listado desplegable
    responsable_id = SelectField(
        'Responsable *',
        coerce=int,
        validators=[DataRequired(message='Debe seleccionar un responsable')],
        description='Seleccione el responsable de la actividad'
    )
    
    
    
    # Tipo de actividad (obligatorio) - Listado desplegable
    tipo_actividad_id = SelectField(
        'Tipo de Actividad *',
        coerce=int,
        validators=[DataRequired(message='Debe seleccionar un tipo de actividad')],
        description='Seleccione el tipo de actividad realizada'
    )
    
    # Acompañamiento jurídico (obligatorio)
    acompanamiento_juridico = BooleanField(
        '¿En la jornada se contó con acompañamiento del área jurídica? *',
        validators=[DataRequired(message='Debe indicar si contó con acompañamiento jurídico')],
        description='Marque si contó con acompañamiento del área jurídica'
    )
    
    # Participantes (múltiple selección) - Listado desplegable
    participantes_ids = SelectMultipleField(
        'Participantes *',
        coerce=int,
        validators=[DataRequired(message='Debe seleccionar al menos un participante')],
        description='Seleccione todos los participantes de la actividad'
    )
    
    # Entidades (múltiple selección) - Listado desplegable
    entidades_ids = SelectMultipleField(
        '¿Con qué entidades contó? *',
        coerce=int,
        validators=[DataRequired(message='Debe seleccionar al menos una entidad')],
        description='Seleccione todas las entidades que acompañaron la actividad'
    )
    
    # Observaciones
    observaciones = TextAreaField(
        'Observaciones',
        validators=[Optional()],
        description='Información adicional o comentarios sobre la actividad (opcional)'
    )
    
    # RESULTADOS (al menos uno debe ser seleccionado)
    cambuches_levantados = IntegerField(
        '# Cambuches levantados',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    armas_blancas_decomisadas = IntegerField(
        '# Armas blancas decomisadas',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    armas_fuego_decomisadas = IntegerField(
        '# Armas de fuego decomisadas',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    requisas = IntegerField(
        '# Requisas',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    sellamientos_establecimientos = IntegerField(
        '# Sellamientos de establecimientos',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    sensibilizaciones = IntegerField(
        '# Sensibilizaciones',
        validators=[Optional(), NumberRange(min=0, message='El número debe ser mayor o igual a 0')],
        default=0
    )
    
    otra_descripcion = StringField(
        'Otra (¿cuál?)',
        validators=[Optional()],
        description='Describa otra actividad realizada (opcional)'
    )
    

    
    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        # Las opciones se cargarán dinámicamente desde la base de datos
        self.responsable_id.choices = []

        self.tipo_actividad_id.choices = []
        self.participantes_ids.choices = []
        self.entidades_ids.choices = []
    
    def validate(self):
        """Validación personalizada del formulario"""
        if not super(ReporteForm, self).validate():
            return False
        
        # Validar que al menos un resultado tenga un valor mayor a 0
        resultados = [
            self.cambuches_levantados.data or 0,
            self.armas_blancas_decomisadas.data or 0,
            self.armas_fuego_decomisadas.data or 0,
            self.requisas.data or 0,
            self.sellamientos_establecimientos.data or 0,
            self.sensibilizaciones.data or 0
        ]
        
        if all(resultado == 0 for resultado in resultados) and not self.otra_descripcion.data:
            raise ValidationError('Debe seleccionar al menos un resultado de la actividad')
        
        return True
