// Variables globales
let datosGlobales = [];

// Menú lateral (drawer)
const menuBtn = document.getElementById('menu-btn');
const sideMenu = document.getElementById('side-menu');
const closeMenu = document.getElementById('close-menu');
const menuOverlay = document.getElementById('menu-overlay');

// Event listeners del menú
menuBtn.addEventListener('click', function() { 
    sideMenu.classList.add('open'); 
    menuOverlay.classList.add('open'); 
});

closeMenu.addEventListener('click', function() { 
    sideMenu.classList.remove('open'); 
    menuOverlay.classList.remove('open'); 
});

menuOverlay.addEventListener('click', function() { 
    sideMenu.classList.remove('open'); 
    menuOverlay.classList.remove('open'); 
});

// Función para inicializar el menú lateral
function initMenu() {
    const menuOptions = document.getElementById('menu-options');
    
    // Crear el botón del Barrio San Bernardo
    const li = document.createElement('li');
    li.innerHTML = '<i class="fas fa-map-marker-alt"></i> Barrio San Bernardo';
    li.addEventListener('click', () => {
        // Cerrar menú después de hacer clic
        sideMenu.classList.remove('open');
        menuOverlay.classList.remove('open');
        
        console.log('Mostrando Dashboard del Barrio San Bernardo');
    });
    menuOptions.appendChild(li);
}

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
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar menú lateral
    initMenu();
    
    // Cargar datos iniciales
    loadData();
}); 