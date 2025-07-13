// Variables globales
let datosGlobales = [];

// --- Eliminado código de menú hamburguesa y overlay para evitar conflictos ---

// Funciones de utilidad
function showError(message) {
    const errorContainer = document.getElementById('error-container');
    errorContainer.innerHTML = `<div class="error">${message}</div>`;
    errorContainer.style.display = 'block';
    hideLoading();
}

function hideLoading() { 
    document.getElementById('loading').style.display = 'none'; 
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

// Función para establecer última actualización
function setLastUpdate(timestamp) {
    const lastUpdateText = document.getElementById('last-update-text');
    if (timestamp) {
        const date = new Date(timestamp);
        lastUpdateText.textContent = date.toLocaleString('es-CO');
    } else {
        lastUpdateText.textContent = 'No disponible';
    }
}

// Inicialización cuando el DOM esté listo
// document.addEventListener('DOMContentLoaded', function() {
//     // Inicializar menú lateral
//     initMenu();
    
//     // Cargar datos iniciales
//     loadData();
// }); 