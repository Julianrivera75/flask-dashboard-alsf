from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models.user import User, db

class LoginForm(FlaskForm):
    """Formulario de login"""
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo electrónico es requerido'),
        Email(message='Por favor ingrese un correo electrónico válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida')
    ])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    """Formulario de registro"""
    first_name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
    ])
    last_name = StringField('Apellido', validators=[
        DataRequired(message='El apellido es requerido'),
        Length(min=2, max=50, message='El apellido debe tener entre 2 y 50 caracteres')
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo electrónico es requerido'),
        Email(message='Por favor ingrese un correo electrónico válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debe confirmar la contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')
    
    def validate_email(self, email):
        """Valida que el email no esté ya registrado"""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor use otro.')

class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña"""
    current_password = PasswordField('Contraseña Actual', validators=[
        DataRequired(message='La contraseña actual es requerida')
    ])
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La nueva contraseña es requerida'),
        Length(min=8, message='La nueva contraseña debe tener al menos 8 caracteres')
    ])
    confirm_new_password = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(message='Debe confirmar la nueva contraseña'),
        EqualTo('new_password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Cambiar Contraseña')

class ResetPasswordRequestForm(FlaskForm):
    """Formulario para solicitar reset de contraseña"""
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo electrónico es requerido'),
        Email(message='Por favor ingrese un correo electrónico válido')
    ])
    submit = SubmitField('Solicitar Reset de Contraseña')

class ResetPasswordForm(FlaskForm):
    """Formulario para reset de contraseña"""
    password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La nueva contraseña es requerida'),
        Length(min=8, message='La nueva contraseña debe tener al menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(message='Debe confirmar la nueva contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Resetear Contraseña') 