from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from forms.auth_forms import LoginForm, RegistrationForm, ChangePasswordForm
from models.user import User, db
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para el login de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Correo electrónico o contraseña incorrectos', 'error')
            if user:
                user.increment_failed_attempts()
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Su cuenta ha sido desactivada. Contacte al administrador.', 'error')
            return redirect(url_for('auth.login'))
        
        if user.is_locked():
            flash('Su cuenta está temporalmente bloqueada debido a múltiples intentos fallidos. Intente más tarde.', 'error')
            return redirect(url_for('auth.login'))
        
        # Login exitoso
        login_user(user, remember=form.remember_me.data)
        user.reset_failed_attempts()
        user.update_last_login()
        
        # Redirigir al usuario a la página que intentaba acceder
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        
        flash(f'¡Bienvenido, {user.get_full_name()}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión"""
    logout_user()
    flash('Ha cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.add(user)
            db.session.commit()
            
            flash('¡Registro exitoso! Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario. Por favor intente nuevamente.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', title='Registrarse', form=form)

@auth.route('/profile')
@login_required
def profile():
    """Ruta para ver el perfil del usuario"""
    return render_template('auth/profile.html', title='Mi Perfil')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Ruta para cambiar contraseña"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('La contraseña actual es incorrecta.', 'error')
            return redirect(url_for('auth.change_password'))
        
        try:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Su contraseña ha sido actualizada exitosamente.', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error al cambiar la contraseña. Por favor intente nuevamente.', 'error')
            return redirect(url_for('auth.change_password'))
    
    return render_template('auth/change_password.html', title='Cambiar Contraseña', form=form)

@auth.route('/admin/users')
@login_required
def admin_users():
    """Ruta para administrar usuarios (solo admin)"""
    if not current_user.is_admin():
        flash('No tiene permisos para acceder a esta página.', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('auth/admin_users.html', title='Administrar Usuarios', users=users)

@auth.route('/admin/user/<int:user_id>/toggle-status')
@login_required
def toggle_user_status(user_id):
    """Ruta para activar/desactivar usuarios (solo admin)"""
    if not current_user.is_admin():
        flash('No tiene permisos para realizar esta acción.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puede desactivar su propia cuenta.', 'error')
        return redirect(url_for('auth.admin_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activada' if user.is_active else 'desactivada'
    flash(f'La cuenta de {user.get_full_name()} ha sido {status}.', 'success')
    return redirect(url_for('auth.admin_users')) 