"""
Formulario para registrar acciones de residuos
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from datetime import date
from models.acciones_residuos import LOCALIDADES_VALIDAS


class AccionResiduosForm(FlaskForm):
    """Formulario para registrar acciones de mitigación de residuos"""
    
    localidad = SelectField(
        'Localidad',
        choices=[('', 'Seleccione una localidad')] + [(loc, loc) for loc in LOCALIDADES_VALIDAS],
        validators=[DataRequired(message='Debe seleccionar una localidad')],
        description='Seleccione la localidad donde se realizaron las acciones'
    )
    
    numero_operativos = IntegerField(
        'Número de Operativos Realizados',
        validators=[
            DataRequired(message='El número de operativos es requerido'),
            NumberRange(min=0, message='El número de operativos debe ser mayor o igual a 0')
        ],
        default=0,
        description='Ingrese el número de operativos realizados'
    )
    
    numero_comparendos = IntegerField(
        'Número de Comparendos Realizados',
        validators=[
            DataRequired(message='El número de comparendos es requerido'),
            NumberRange(min=0, message='El número de comparendos debe ser mayor o igual a 0')
        ],
        default=0,
        description='Ingrese el número de comparendos realizados'
    )
    
    numero_sensibilizaciones = IntegerField(
        'Número de Sensibilizaciones Realizadas',
        validators=[
            DataRequired(message='El número de sensibilizaciones es requerido'),
            NumberRange(min=0, message='El número de sensibilizaciones debe ser mayor o igual a 0')
        ],
        default=0,
        description='Ingrese el número de sensibilizaciones realizadas'
    )
    
    fecha_operacion = DateField(
        'Fecha de la Operación',
        validators=[DataRequired(message='La fecha de operación es requerida')],
        default=date.today,
        description='Seleccione la fecha en que se realizaron las acciones'
    )
    
    usuario_registro = StringField(
        'Usuario que Registra',
        validators=[Optional()],
        description='Nombre de la persona que registra la información (opcional)'
    )
    
    observaciones = TextAreaField(
        'Observaciones',
        validators=[Optional()],
        description='Observaciones adicionales sobre las acciones realizadas (opcional)',
        render_kw={'rows': 4}
    )
    
    submit = SubmitField('Registrar Acción')
    
    def validate_fecha_operacion(self, field):
        """Validar que la fecha no sea futura"""
        if field.data and field.data > date.today():
            raise ValidationError('La fecha de operación no puede ser futura')
    
    def validate_localidad(self, field):
        """Validar que la localidad sea una de las válidas"""
        if field.data and field.data not in LOCALIDADES_VALIDAS:
            raise ValidationError('Debe seleccionar una localidad válida')

