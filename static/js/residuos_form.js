/**
 * JavaScript para validación del formulario de residuos
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-residuos');
    
    if (!form) {
        console.warn('Formulario no encontrado');
        return;
    }
    
    // Validación del lado del cliente
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
        });
        
        // Validar fecha no futura
        const fechaInput = form.querySelector('input[type="date"]');
        if (fechaInput) {
            fechaInput.addEventListener('change', function() {
                const fechaSeleccionada = new Date(this.value);
                const hoy = new Date();
                hoy.setHours(0, 0, 0, 0);
                
                if (fechaSeleccionada > hoy) {
                    this.setCustomValidity('La fecha de operación no puede ser futura');
                    this.classList.add('is-invalid');
                } else {
                    this.setCustomValidity('');
                    this.classList.remove('is-invalid');
                }
            });
        }
        
        // Validar números no negativos
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value < 0) {
                    this.value = 0;
                }
            });
            
            input.addEventListener('blur', function() {
                if (this.value === '' || this.value < 0) {
                    this.value = 0;
                }
            });
        });
    }
    
    // Auto-ocultar mensajes flash después de 5 segundos
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Botón de cerrar mensajes
    const closeButtons = document.querySelectorAll('.btn-close');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }
        });
    });
});

/**
 * Validar formulario antes de enviar
 */
function validateForm() {
    const form = document.getElementById('form-residuos');
    if (!form) return false;
    
    let isValid = true;
    
    // Validar localidad
    const localidad = form.querySelector('select[name="localidad"]');
    if (localidad && !localidad.value) {
        showFieldError(localidad, 'Debe seleccionar una localidad');
        isValid = false;
    } else {
        clearFieldError(localidad);
    }
    
    // Validar fecha
    const fecha = form.querySelector('input[type="date"]');
    if (fecha) {
        if (!fecha.value) {
            showFieldError(fecha, 'La fecha de operación es requerida');
            isValid = false;
        } else {
            const fechaSeleccionada = new Date(fecha.value);
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            
            if (fechaSeleccionada > hoy) {
                showFieldError(fecha, 'La fecha de operación no puede ser futura');
                isValid = false;
            } else {
                clearFieldError(fecha);
            }
        }
    }
    
    // Validar números
    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        if (!input.value || input.value < 0) {
            input.value = 0;
        }
    });
    
    return isValid;
}

/**
 * Mostrar error en un campo
 */
function showFieldError(field, message) {
    if (!field) return;
    
    field.classList.add('is-invalid');
    
    // Remover mensaje de error anterior
    const existingError = field.parentElement.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar nuevo mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentElement.appendChild(errorDiv);
}

/**
 * Limpiar error de un campo
 */
function clearFieldError(field) {
    if (!field) return;
    
    field.classList.remove('is-invalid');
    const errorDiv = field.parentElement.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}
