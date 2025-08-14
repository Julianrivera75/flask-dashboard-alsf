from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from models.reporte import Categoria

class ReporteForm(FlaskForm):
    """Formulario para crear/editar reportes"""
    
    # Campos principales
    actividad = TextAreaField('Actividad', validators=[
        DataRequired(message='La actividad es obligatoria'),
        Length(min=10, max=1000, message='La actividad debe tener entre 10 y 1000 caracteres')
    ])
    
    observaciones = TextAreaField('Observaciones', validators=[
        Optional(),
        Length(max=2000, message='Las observaciones no pueden exceder 2000 caracteres')
    ])
    
    # Categoría
    categoria_id = SelectField('Categoría', coerce=int, validators=[
        DataRequired(message='Debe seleccionar una categoría')
    ])
    
    # Georreferenciación
    latitud = FloatField('Latitud', validators=[
        DataRequired(message='La latitud es obligatoria'),
        NumberRange(min=-90, max=90, message='La latitud debe estar entre -90 y 90')
    ])
    
    longitud = FloatField('Longitud', validators=[
        DataRequired(message='La longitud es obligatoria'),
        NumberRange(min=-180, max=180, message='La longitud debe estar entre -180 y 180')
    ])
    
    direccion = StringField('Dirección', validators=[
        Optional(),
        Length(max=300, message='La dirección no puede exceder 300 caracteres')
    ])
    
    # Archivos
    acta_pdf = FileField('Acta (PDF)', validators=[
        FileRequired(message='El acta es obligatoria'),
        FileAllowed(['pdf'], message='Solo se permiten archivos PDF')
    ])
    
    foto_1 = FileField('Foto 1', validators=[
        FileRequired(message='La primera foto es obligatoria'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], message='Solo se permiten imágenes')
    ])
    
    foto_2 = FileField('Foto 2', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], message='Solo se permiten imágenes')
    ])
    
    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.categoria_id.choices = self._get_categorias()
    
    def _get_categorias(self):
        """Obtiene las categorías activas para el formulario"""
        try:
            categorias = Categoria.query.filter_by(activo=True).order_by(Categoria.orden, Categoria.nombre).all()
            return [(cat.id, cat.nombre) for cat in categorias]
        except Exception:
            # Si hay error en la base de datos, retornar lista vacía
            return []
    
    def validate(self):
        """Validación personalizada del formulario"""
        if not super(ReporteForm, self).validate():
            return False
        
        # Validar que las coordenadas estén en un rango razonable para Bogotá
        # Bogotá está aproximadamente entre lat: 4.4-4.8 y lon: -74.2--73.9
        if self.latitud.data < 4.0 or self.latitud.data > 5.0:
            self.latitud.errors.append('La latitud debe estar en el rango de Bogotá (4.0-5.0)')
            return False
        
        if self.longitud.data < -74.5 or self.longitud.data > -73.5:
            self.longitud.errors.append('La longitud debe estar en el rango de Bogotá (-74.5 a -73.5)')
            return False
        
        return True
