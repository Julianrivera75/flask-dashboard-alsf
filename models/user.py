from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de usuario para autenticación"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, user, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    def __init__(self, email, password, first_name, last_name, role='user'):
        self.email = email.lower()
        self.password_hash = self._hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
    
    def _hash_password(self, password):
        """Genera hash seguro de la contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def set_password(self, new_password):
        """Actualiza la contraseña del usuario"""
        self.password_hash = self._hash_password(new_password)
    
    def is_locked(self):
        """Verifica si la cuenta está bloqueada"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    def increment_failed_attempts(self):
        """Incrementa los intentos fallidos de login"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            # Bloquear cuenta por 30 minutos
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
    
    def reset_failed_attempts(self):
        """Resetea los intentos fallidos de login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()
    
    def update_last_login(self):
        """Actualiza la fecha del último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>' 