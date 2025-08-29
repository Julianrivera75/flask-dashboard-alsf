/**
 * JavaScript para el formulario de 1000 Acciones en 1 Día
 * Utiliza funciones comunes de acciones_1000_common.js
 */

// Variables específicas del formulario
let marker;

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    initializeMap();
    initializeFileUpload();
    setupFormValidation();
});

/**
 * Inicializar el formulario
 */
function initializeForm() {
    // Mostrar/ocultar campo "otro" área según selección
    const areaResponsable = document.getElementById('area_responsable');
    const areaOtroGroup = document.getElementById('area_otro_group');
    
    if (areaResponsable && areaOtroGroup) {
        areaResponsable.addEventListener('change', function() {
            if (this.value === 'otro') {
                areaOtroGroup.style.display = 'block';
                document.getElementById('area_otro').required = true;
            } else {
                areaOtroGroup.style.display = 'none';
                document.getElementById('area_otro').required = false;
                document.getElementById('area_otro').value = '';
            }
        });
    }
    
    // Manejar envío del formulario
    const form = document.getElementById('acciones1000Form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

/**
 * Inicializar el mapa de Leaflet
 */
function initializeMap() {
    // Coordenadas de Bogotá (centro aproximado)
    const bogotaCenter = [4.7110, -74.0721];
    
    // Crear mapa
    map = L.map('mapa-formulario').setView(bogotaCenter, 11);
    
    // Agregar capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Agregar capa de sectores catastrales (KML) usando función común
    addSectoresCatastrales(map, 'formulario');
    
    // Centrar el mapa en los sectores catastrales después de cargarlos
    setTimeout(() => {
        centerMapOnSectores();
    }, 1000); // Esperar 1 segundo para que se carguen los sectores
    
    // Evento de clic en el mapa
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Actualizar marcador
        if (marker) {
            map.removeLayer(marker);
        }
        
        marker = L.marker([lat, lng]).addTo(map);
        
        // Actualizar campos ocultos
        document.getElementById('latitud').value = lat;
        document.getElementById('longitud').value = lng;
        
        selectedLocation = true;
        
        // Mostrar mensaje de confirmación
        showAlert('Ubicación seleccionada', `Lat: ${lat.toFixed(6)}, Lng: ${lng.toFixed(6)}`, 'success');
    });
    
    // Agregar controles adicionales
    addMapControls();
}

/**
 * Agregar controles adicionales al mapa
 */
function addMapControls() {
    // Botón para centrar en Bogotá
    const centerButton = L.control({ position: 'topright' });
    centerButton.onAdd = function() {
        const div = L.DomUtil.create('div', 'leaflet-control leaflet-bar');
        div.innerHTML = '<button onclick="centerMapForm()" title="Centrar en Bogotá" style="width: 30px; height: 30px; background: white; border: 1px solid #ccc; cursor: pointer;"><i class="fas fa-crosshairs"></i></button>';
        return div;
    };
    centerButton.addTo(map);
}

/**
 * Centrar mapa del formulario en Bogotá
 */
function centerMapForm() {
    centerMap(map);
}

/**
 * Inicializar carga de archivos
 */
function initializeFileUpload() {
    const fileInput = document.getElementById('fotos');
    const filePreview = document.getElementById('file-preview');
    
    if (fileInput && filePreview) {
        fileInput.addEventListener('change', function(e) {
            handleFileSelection(e.target.files, filePreview);
        });
    }
}

/**
 * Manejar selección de archivos
 */
function handleFileSelection(files, previewContainer) {
    const MAX_FILES = 4;
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    
    // Validar número máximo de archivos
    if (files.length > MAX_FILES) {
        showAlert('Error', `Puedes seleccionar máximo ${MAX_FILES} imágenes`, 'error');
        // Limpiar input y vista previa
        document.getElementById('fotos').value = '';
        previewContainer.innerHTML = '';
        updateFileInfo(0);
        return;
    }
    
    // Validar cada archivo
    const validFiles = [];
    const invalidFiles = [];
    
    Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) {
            invalidFiles.push(`${file.name} (no es una imagen)`);
        } else if (file.size > MAX_FILE_SIZE) {
            invalidFiles.push(`${file.name} (más de 5MB)`);
        } else {
            validFiles.push(file);
        }
    });
    
    // Mostrar errores si hay archivos inválidos
    if (invalidFiles.length > 0) {
        showAlert('Error', `Archivos inválidos:\n${invalidFiles.join('\n')}`, 'error');
        // Limpiar input y vista previa
        document.getElementById('fotos').value = '';
        previewContainer.innerHTML = '';
        updateFileInfo(0);
        return;
    }
    
    // Limpiar vista previa
    previewContainer.innerHTML = '';
    
    // Mostrar archivos válidos
    validFiles.forEach((file, index) => {
        const reader = new FileReader();
        const previewItem = document.createElement('div');
        previewItem.className = 'file-preview-item';
        
        reader.onload = function(e) {
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <div class="file-details">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
                <button type="button" class="remove-file" onclick="removeFile(${index})" title="Eliminar archivo">
                    <i class="fas fa-times"></i>
                </button>
            `;
        };
        
        reader.readAsDataURL(file);
        previewContainer.appendChild(previewItem);
    });
    
    // Actualizar información de archivos
    updateFileInfo(validFiles.length);
}

/**
 * Eliminar archivo de la vista previa
 */
function removeFile(index) {
    const fileInput = document.getElementById('fotos');
    const dt = new DataTransfer();
    const { files } = fileInput;
    
    for (let i = 0; i < files.length; i++) {
        if (i !== index) {
            dt.items.add(files[i]);
        }
    }
    
    fileInput.files = dt.files;
    handleFileSelection(fileInput.files, document.getElementById('file-preview'));
}

/**
 * Actualizar información de archivos seleccionados
 */
function updateFileInfo(fileCount) {
    const fileCountElement = document.querySelector('.file-count');
    if (fileCountElement) {
        fileCountElement.textContent = `${fileCount} de 4 imágenes seleccionadas`;
    }
}

/**
 * Configurar validación del formulario
 */
function setupFormValidation() {
    const form = document.getElementById('acciones1000Form');
    
    if (form) {
        // Validar antes del envío
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
        });
        
        // Validación en tiempo real
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', function() {
                validateField(this);
            });
        });
    }
}

/**
 * Validar campo individual
 */
function validateField(field) {
    const errorDiv = field.parentNode.querySelector('.error-message');
    
    if (errorDiv) {
        errorDiv.remove();
    }
    
    if (field.hasAttribute('required') && !field.value.trim()) {
        showFieldError(field, 'Este campo es obligatorio');
        return false;
    }
    
    // Validaciones específicas
    if (field.id === 'personas_impactadas') {
        const value = parseInt(field.value);
        if (isNaN(value) || value < 1) {
            showFieldError(field, 'Debe ser un número mayor a 0');
            return false;
        }
    }
    
    if (field.id === 'area_otro' && document.getElementById('area_responsable').value === 'otro') {
        if (!field.value.trim()) {
            showFieldError(field, 'Debe especificar otra área');
            return false;
        }
    }
    
    return true;
}

/**
 * Mostrar error de campo
 */
function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<span>${message}</span>`;
    
    field.parentNode.appendChild(errorDiv);
    field.classList.add('error');
}

/**
 * Validar formulario completo
 */
function validateForm() {
    let isValid = true;
    const form = document.getElementById('acciones1000Form');
    
    // Limpiar errores previos
    form.querySelectorAll('.error-message').forEach(error => error.remove());
    form.querySelectorAll('.form-control').forEach(field => field.classList.remove('error'));
    
    // Validar campos requeridos
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    // Validar ubicación en mapa
    if (!selectedLocation) {
        showAlert('Error de validación', 'Debe seleccionar una ubicación en el mapa', 'error');
        isValid = false;
    }
    
    // Validar archivos
    const fileInput = document.getElementById('fotos');
    if (!fileInput.files || fileInput.files.length === 0) {
        showAlert('Error de validación', 'Debe seleccionar al menos una foto', 'error');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Manejar envío del formulario
 */
function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        return false;
    }
    
    // Mostrar estado de carga
    const submitBtn = document.getElementById('submit-btn');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Enviando...';
    
    // Crear FormData
    const formData = new FormData(e.target);
    
    // Enviar formulario
    fetch(e.target.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Verificar si la respuesta es JSON válido
        if (!response.ok) {
            if (response.status === 400) {
                // Error de validación o CSRF
                return response.json().then(data => {
                    throw new Error(data.message || 'Error de validación');
                });
            } else {
                throw new Error(`Error del servidor: ${response.status}`);
            }
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showAlert('¡Éxito!', data.message, 'success');
            resetForm();
        } else {
            showAlert('Error', data.message || 'Error al procesar el formulario', 'error');
            
            // Mostrar errores específicos si existen
            if (data.errors) {
                Object.keys(data.errors).forEach(fieldName => {
                    const field = document.getElementById(fieldName);
                    if (field) {
                        showFieldError(field, data.errors[fieldName]);
                    }
                });
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Verificar si es un error de CSRF
        if (error.message && error.message.includes('CSRF')) {
            showAlert('Error de Seguridad', 'El token de seguridad ha expirado. Por favor, recargue la página e intente nuevamente.', 'error');
            
            // Opcional: recargar la página automáticamente
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        } else {
            showAlert('Error', 'Error de conexión. Intente nuevamente.', 'error');
        }
    })
    .finally(() => {
        // Restaurar botón
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

/**
 * Resetear formulario
 */
function resetForm(showMessage = false) {
    const form = document.getElementById('acciones1000Form');
    form.reset();
    
    // Limpiar errores
    form.querySelectorAll('.error-message').forEach(error => error.remove());
    form.querySelectorAll('.form-control').forEach(field => field.classList.remove('error'));
    
    // Ocultar campo "otro" área
    document.getElementById('area_otro_group').style.display = 'none';
    
    // Limpiar mapa
    if (marker) {
        map.removeLayer(marker);
        marker = null;
    }
    selectedLocation = false;
    
    // Limpiar vista previa de archivos
    document.getElementById('file-preview').innerHTML = '';
    
    // Limpiar información de archivos
    updateFileInfo(0);
    
    // Limpiar campos ocultos
    document.getElementById('latitud').value = '';
    document.getElementById('longitud').value = '';
    
    // Solo mostrar mensaje si se solicita explícitamente
    if (showMessage) {
        showAlert('Formulario limpiado', 'El formulario ha sido limpiado correctamente', 'info');
    }
}

/**
 * Centrar mapa en los sectores catastrales
 */
function centerMapOnSectores() {
    try {
        // Intentar obtener los límites de las capas del mapa
        const layers = map._layers;
        let bounds = null;
        
        // Buscar capas que puedan tener límites (como KML o marcadores)
        Object.values(layers).forEach(layer => {
            if (layer.getBounds && typeof layer.getBounds === 'function') {
                try {
                    const layerBounds = layer.getBounds();
                    if (layerBounds && layerBounds.isValid && layerBounds.isValid()) {
                        if (!bounds) {
                            bounds = layerBounds;
                        } else {
                            bounds.extend(layerBounds);
                        }
                    }
                } catch (error) {
                    // Ignorar errores en capas individuales
                }
            }
        });
        
        // Si se encontraron límites, centrar el mapa
        if (bounds && bounds.isValid && bounds.isValid()) {
            map.fitBounds(bounds, { padding: [20, 20] });
            console.log('Mapa del formulario centrado en sectores catastrales');
        } else {
            // Fallback: centrar en Bogotá con zoom apropiado
            const bogotaCenter = [4.7110, -74.0721];
            map.setView(bogotaCenter, 11);
            console.log('Mapa del formulario centrado en Bogotá (fallback)');
        }
    } catch (error) {
        console.log('Error al centrar mapa en sectores, usando vista por defecto');
        const bogotaCenter = [4.7110, -74.0721];
        map.setView(bogotaCenter, 11);
    }
}

// Exportar funciones específicas del formulario para uso global
window.resetForm = resetForm;
window.removeFile = removeFile;
window.centerMapForm = centerMapForm;
window.centerMapOnSectores = centerMapOnSectores;
