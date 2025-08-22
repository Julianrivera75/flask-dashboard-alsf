import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class FileService:
    """Servicio para manejar archivos (PDF y fotos)"""
    
    def __init__(self, upload_folder='static/uploads/reportes'):
        self.upload_folder = upload_folder
        self.allowed_extensions = {
            'pdf': {'pdf'},
            'foto': {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        }
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def allowed_file(self, filename, tipo_archivo):
        """Verifica si el archivo tiene una extensión permitida"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in self.allowed_extensions.get(tipo_archivo, set())
    
    def generate_filename(self, original_filename, tipo_archivo, reporte_id):
        """Genera un nombre único para el archivo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        ext = original_filename.rsplit('.', 1)[1].lower()
        
        if tipo_archivo == 'pdf':
            return f"{timestamp}_acta_{reporte_id}_{unique_id}.{ext}"
        elif tipo_archivo == 'foto':
            return f"{timestamp}_foto_{reporte_id}_{unique_id}.{ext}"
        else:
            return f"{timestamp}_{tipo_archivo}_{reporte_id}_{unique_id}.{ext}"
    
    def create_upload_path(self, reporte_id):
        """Crea la ruta de subida organizada por fecha y reporte"""
        today = datetime.now()
        year_month = today.strftime('%Y/%m')
        path = os.path.join(self.upload_folder, year_month, f'reporte_{reporte_id}')
        
        # Crear directorios si no existen
        os.makedirs(path, exist_ok=True)
        return path
    
    def process_image(self, file_path, max_size=(1920, 1080)):
        """Procesa y optimiza una imagen"""
        try:
            with Image.open(file_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Guardar optimizado
                img.save(file_path, quality=85, optimize=True)
                
                return f"{img.size[0]}x{img.size[1]}"
        except Exception as e:
            logger.error(f"Error procesando imagen {file_path}: {str(e)}")
            return None
    
    def save_file(self, file, tipo_archivo, reporte_id):
        """Guarda un archivo y retorna la información"""
        if not file or not file.filename:
            return None
        
        if not self.allowed_file(file.filename, tipo_archivo):
            raise ValueError(f"Tipo de archivo no permitido para {tipo_archivo}")
        
        # Verificar tamaño
        file.seek(0, 2)  # Ir al final del archivo
        file_size = file.tell()
        file.seek(0)  # Volver al inicio
        
        if file_size > self.max_file_size:
            raise ValueError(f"Archivo demasiado grande. Máximo {self.max_file_size // (1024*1024)}MB")
        
        # Generar nombre y ruta
        nombre_original = secure_filename(file.filename)
        nombre_archivo = self.generate_filename(nombre_original, tipo_archivo, reporte_id)
        upload_path = self.create_upload_path(reporte_id)
        file_path = os.path.join(upload_path, nombre_archivo)
        
        # Guardar archivo
        file.save(file_path)
        
        # Procesar imagen si es necesario
        dimensiones = None
        if tipo_archivo == 'foto':
            dimensiones = self.process_image(file_path)
        
        return {
            'nombre_original': nombre_original,
            'nombre_archivo': nombre_archivo,
            'ruta_archivo': file_path,
            'tamaño_bytes': file_size,
            'tipo_mime': file.content_type,
            'dimensiones': dimensiones
        }
    
    def delete_file(self, file_path):
        """Elimina un archivo del sistema"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            logger.error(f"Error eliminando archivo {file_path}: {str(e)}")
        return False
    
    def get_file_url(self, file_path):
        """Genera la URL pública para un archivo"""
        # Para desarrollo, usar ruta relativa
        if file_path.startswith('static/'):
            return '/' + file_path
        return file_path


