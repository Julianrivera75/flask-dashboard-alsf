# Sistema de Autenticación - Indicadores de Gestión

## 📋 Descripción

Este sistema de autenticación proporciona un control de acceso seguro para la aplicación de Indicadores de Gestión de la Localidad de Santa Fé. Incluye funcionalidades de login, registro, gestión de usuarios y roles.

## 🚀 Características

### ✅ Funcionalidades Implementadas

- **🔐 Autenticación segura** con bcrypt para hash de contraseñas
- **👥 Gestión de usuarios** con roles (admin, user, viewer)
- **🔒 Protección contra ataques** de fuerza bruta
- **📧 Validación de email** con formato correcto
- **🔄 Sesiones persistentes** con opción "Recordarme"
- **👤 Perfiles de usuario** con información personal
- **🔑 Cambio de contraseña** seguro
- **⚡ Bloqueo automático** de cuentas después de 5 intentos fallidos
- **📊 Panel de administración** para gestión de usuarios
- **🎨 Interfaz moderna** y responsiva

### 🛡️ Medidas de Seguridad

- **Hash de contraseñas**: bcrypt con salt único
- **Protección CSRF**: Tokens en formularios
- **Sesiones seguras**: Configuración de cookies HTTPOnly
- **Validación de entrada**: Sanitización de datos
- **Rate limiting**: Bloqueo temporal de cuentas
- **Logs de actividad**: Registro de intentos de login

## 📦 Instalación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear o actualizar el archivo `credentials/config.env`:

```env
# Configuración de la aplicación
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
SHEET_ID=tu-google-sheet-id

# Configuración de base de datos (opcional)
DATABASE_URL=sqlite:///app.db
```

### 3. Inicializar la Base de Datos

```bash
python init_auth.py
```

Seleccione la opción **1** para inicializar la base de datos y crear usuarios iniciales.

## 👤 Usuarios por Defecto

Después de la inicialización, se crean los siguientes usuarios:

### 🔧 Administrador
- **Email**: `admin@example.com`
- **Contraseña**: `admin123456`
- **Rol**: `admin`
- **⚠️ IMPORTANTE**: Cambie esta contraseña después del primer login

### 👥 Usuarios de Ejemplo
- **Email**: `usuario1@example.com` / **Contraseña**: `usuario123`
- **Email**: `usuario2@example.com` / **Contraseña**: `usuario123`
- **Email**: `viewer@example.com` / **Contraseña**: `viewer123`

## 🏃‍♂️ Ejecución

### Desarrollo
```bash
python app_with_auth.py
```

### Producción
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_with_auth:app
```

## 📱 Uso del Sistema

### 🔐 Login
1. Acceda a `http://localhost:5000/auth/login`
2. Ingrese su email y contraseña
3. Opcional: Marque "Recordarme" para sesión persistente
4. Haga clic en "Iniciar Sesión"

### 📝 Registro
1. Acceda a `http://localhost:5000/auth/register`
2. Complete el formulario con sus datos
3. La contraseña debe tener al menos 8 caracteres
4. Haga clic en "Registrarse"

### 👤 Perfil de Usuario
- **Ver perfil**: `http://localhost:5000/auth/profile`
- **Cambiar contraseña**: `http://localhost:5000/auth/change-password`

### 🔧 Panel de Administración
- **Gestionar usuarios**: `http://localhost:5000/auth/admin/users` (solo admin)

## 🎭 Roles de Usuario

### 👑 Administrador (`admin`)
- Acceso completo a todas las funcionalidades
- Gestión de usuarios (activar/desactivar)
- Panel de administración
- Puede cambiar roles de usuarios

### 👤 Usuario (`user`)
- Acceso a todas las páginas de la aplicación
- Puede ver y actualizar su perfil
- Puede cambiar su contraseña
- No puede gestionar otros usuarios

### 👁️ Visualizador (`viewer`)
- Acceso de solo lectura a los datos
- No puede realizar cambios
- Ideal para consultas y reportes

## 🛠️ Herramientas de Administración

### Script de Inicialización (`init_auth.py`)

```bash
python init_auth.py
```

**Opciones disponibles:**
1. **Inicializar base de datos**: Crea tablas y usuarios iniciales
2. **Crear administrador**: Crea un nuevo usuario administrador
3. **Resetear contraseña**: Cambia la contraseña de un administrador
4. **Ver usuarios**: Lista todos los usuarios del sistema
5. **Salir**: Cierra el script

### Ejemplos de Uso

```bash
# Crear un nuevo administrador
python init_auth.py
# Seleccione opción 2

# Ver usuarios existentes
python init_auth.py
# Seleccione opción 4
```

## 🔧 Configuración Avanzada

### Configuración de Base de Datos

En `config.py` puede modificar:

```python
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'  # SQLite para desarrollo
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/db'  # PostgreSQL para producción
```

### Configuración de Seguridad

```python
class Config:
    # Duración de la sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Configuración de cookies
    SESSION_COOKIE_SECURE = True  # Solo HTTPS en producción
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Protección CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora
```

## 🚨 Seguridad

### Recomendaciones de Producción

1. **🔑 Cambiar SECRET_KEY**: Use una clave secreta fuerte y única
2. **🔒 HTTPS**: Configure SSL/TLS en producción
3. **🗄️ Base de datos**: Use PostgreSQL o MySQL en lugar de SQLite
4. **📧 Email**: Configure un servidor SMTP para notificaciones
5. **📊 Logs**: Implemente logging de seguridad
6. **🔄 Backups**: Realice backups regulares de la base de datos

### Configuración de Seguridad

```python
# En producción, active estas configuraciones:
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
WTF_CSRF_ENABLED = True
```

## 🐛 Solución de Problemas

### Error: "No module named 'bcrypt'"
```bash
pip install bcrypt
```

### Error: "Database is locked"
- Verifique que no hay otras instancias ejecutándose
- Reinicie la aplicación

### Error: "Invalid credentials"
- Verifique que el archivo `credentials.json` existe
- Confirme que las credenciales de Google Sheets son correctas

### Usuario bloqueado
- Espere 30 minutos o use el script para resetear intentos fallidos
- Contacte al administrador

## 📞 Soporte

Para problemas o preguntas:

1. **📖 Documentación**: Revise este README
2. **🐛 Issues**: Reporte bugs en el repositorio
3. **💬 Consultas**: Contacte al equipo de desarrollo

## 📝 Changelog

### v1.0.0 (2024-01-XX)
- ✅ Sistema de autenticación completo
- ✅ Gestión de usuarios y roles
- ✅ Interfaz moderna y responsiva
- ✅ Medidas de seguridad implementadas
- ✅ Herramientas de administración
- ✅ Documentación completa

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](../LICENSE) para detalles.

### Resumen de la Licencia MIT

La Licencia MIT es una licencia de software libre permisiva que permite:

- ✅ **Uso comercial** - Puede usarse en proyectos comerciales
- ✅ **Modificación** - Puede modificarse libremente
- ✅ **Distribución** - Puede distribuirse sin restricciones
- ✅ **Uso privado** - Puede usarse en proyectos privados
- ✅ **Sublicencia** - Puede sublicenciarse bajo otras licencias

**Única condición**: Incluir el aviso de copyright y la licencia en todas las copias o partes sustanciales del software.

Para más información sobre la Licencia MIT, consulta: [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

---

**⚠️ IMPORTANTE**: Este sistema está diseñado para uso interno. En producción, implemente medidas de seguridad adicionales según las políticas de su organización. 