/**
 * Funciones comunes para 1000 Acciones en 1 Día
 * Este archivo contiene funciones compartidas entre el formulario y el mapa
 */

// Variables globales compartidas
let map;
let selectedLocation = false;

// Tipos de actividades disponibles (31 actividades)
const ACTIVIDADES_DISPONIBLES = [
    'Diálogo diferencial LGBTI',
    'Fiesta Mayor',
    'Feria de Emprendedoras y Productoras Locales',
    'Recuperación entornos tramos universitarios - sector las aguas-',
    'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA',
    'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA',
    'Jornada de embellecimiento',
    'Jornada de Protección y Bienestar Animal - PYBA',
    'MES MAYOR',
    'INAUGURACIÓN CENTRO DE EXPERIENCIA TIC',
    'Actividad',
    'Encuentro',
    'Fugate al centro'
];

// Colores para los marcadores según el área
const areaColors = {
    'Ambiente': '#28a745',
    'Seguridad': '#dc3545',
    'Deportes': '#007bff',
    'Participación': '#ffc107',
    'Innovación': '#17a2b8',
    'Planeación': '#6f42c1',
    'otro': '#6c757d'
};

/**
 * Agregar capa de sectores catastrales desde KML
 * @param {Object} mapInstance - Instancia del mapa Leaflet
 * @param {string} context - Contexto donde se llama (formulario/mapa)
 * 
 * En los contextos 'mapa' y 'formulario', se centrará automáticamente en los polígonos azules
 * cuando se carguen exitosamente.
 */
function addSectoresCatastrales(mapInstance, context = 'formulario') {
    try {
        console.log(`Intentando cargar sectores catastrales en el ${context}...`);
        
        // URL del archivo KML de sectores catastrales
        const kmlUrl = '/static/data/SectoresCatastrales.kml';
        
        // Intentar cargar el KML usando la librería omnivore (si está disponible)
        if (typeof omnivore !== 'undefined') {
            console.log(`Librería omnivore disponible, cargando KML en ${context}...`);
            const kmlLayer = omnivore.kml(kmlUrl)
                .on('ready', function() {
                    console.log(`KML de sectores catastrales cargado exitosamente en el ${context}`);
                    
                    // Centrar el mapa en los polígonos del KML cuando estén listos
                    if (context === 'mapa' || context === 'formulario') {
                        try {
                            // Obtener los límites de la capa KML y centrar el mapa
                            const bounds = kmlLayer.getBounds();
                            if (bounds.isValid()) {
                                mapInstance.fitBounds(bounds, { padding: [20, 20] });
                                console.log(`Mapa ${context} centrado en los sectores catastrales`);
                            }
                        } catch (error) {
                            console.log('No se pudieron obtener los límites del KML, usando vista por defecto');
                        }
                    }
                })
                .on('error', function(error) {
                    console.error(`Error al cargar KML en ${context}:`, error);
                    // Fallback: mostrar marcadores de ejemplo
                    addExampleSectores(mapInstance, context);
                });
            kmlLayer.addTo(mapInstance);
        } else {
            // Si omnivore no está disponible, usar marcadores de ejemplo
            console.log(`Librería omnivore no disponible en ${context}, usando marcadores de ejemplo`);
            addExampleSectores(mapInstance, context);
        }
    } catch (error) {
        console.error(`Error al cargar sectores catastrales en ${context}:`, error);
        addExampleSectores(mapInstance, context);
    }
}

/**
 * Agregar sectores catastrales de ejemplo como fallback
 * @param {Object} mapInstance - Instancia del mapa Leaflet
 * @param {string} context - Contexto donde se llama (formulario/mapa)
 */
function addExampleSectores(mapInstance, context = 'formulario') {
    console.log(`Agregando sectores catastrales de ejemplo en ${context}...`);
    
    // Coordenadas aproximadas de sectores catastrales en Bogotá
    const sectores = [
        { lat: 4.7110, lng: -74.0721, nombre: 'Sector Central' },
        { lat: 4.7200, lng: -74.0800, nombre: 'Sector Norte' },
        { lat: 4.7000, lng: -74.0640, nombre: 'Sector Sur' },
        { lat: 4.7150, lng: -74.0600, nombre: 'Sector Este' },
        { lat: 4.7050, lng: -74.0840, nombre: 'Sector Oeste' }
    ];
    
    sectores.forEach(sector => {
        const marker = L.marker([sector.lat, sector.lng], {
            icon: L.divIcon({
                className: 'sector-catastral-marker',
                html: '<div style="background: rgba(0,123,255,0.7); border: 2px solid #007bff; border-radius: 50%; width: 20px; height: 20px;"></div>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            })
        }).addTo(mapInstance);
        
        marker.bindPopup(`<b>Sector Catastral</b><br>${sector.nombre}`);
    });
    
    console.log(`Sectores catastrales de ejemplo agregados al ${context}`);
    
    // Centrar el mapa en los sectores de ejemplo si es el mapa de actividades o formulario
    if (context === 'mapa' || context === 'formulario') {
        try {
            // Crear un grupo con todos los marcadores para obtener los límites
            const markers = [];
            sectores.forEach(sector => {
                const marker = L.marker([sector.lat, sector.lng]);
                markers.push(marker);
            });
            
            const group = L.featureGroup(markers);
            const bounds = group.getBounds();
            if (bounds.isValid()) {
                mapInstance.fitBounds(bounds, { padding: [20, 20] });
                console.log(`Mapa ${context} centrado en los sectores catastrales de ejemplo`);
            }
        } catch (error) {
            console.log('No se pudieron centrar los sectores de ejemplo');
        }
    }
}

/**
 * Centrar mapa en Bogotá
 * @param {Object} mapInstance - Instancia del mapa Leaflet
 */
function centerMap(mapInstance) {
    const bogotaCenter = [4.7110, -74.0721];
    mapInstance.setView(bogotaCenter, 12);
    showAlert('Mapa centrado', 'Mapa centrado en Bogotá', 'info');
}

/**
 * Formatear fecha en hora de Colombia
 * @param {string} dateString - String de fecha
 * @returns {string} Fecha formateada en hora de Colombia
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    try {
        const date = new Date(dateString);
        
        // Formatear en español con hora de Colombia
        return date.toLocaleDateString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'America/Bogota'
        });
    } catch (error) {
        console.error('Error al formatear fecha:', error);
        // Fallback: mostrar fecha original
        return dateString;
    }
}

/**
 * Mostrar alerta
 * @param {string} title - Título de la alerta
 * @param {string} message - Mensaje de la alerta
 * @param {string} type - Tipo de alerta (info, success, error, warning)
 */
function showAlert(title, message, type = 'info') {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: message,
            icon: type,
            confirmButtonColor: '#e4032e',
            confirmButtonText: 'Aceptar'
        });
    } else {
        // Fallback si SweetAlert2 no está disponible
        alert(`${title}: ${message}`);
    }
}

/**
 * Formatear tamaño de archivo
 * @param {number} bytes - Tamaño en bytes
 * @returns {string} Tamaño formateado
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Crear marcador para una actividad
 * @param {Object} activity - Datos de la actividad
 * @param {Object} mapInstance - Instancia del mapa Leaflet
 * @param {Function} clickCallback - Función a ejecutar al hacer clic
 * @returns {Object} Marcador de Leaflet
 */
function createActivityMarker(activity, mapInstance, clickCallback = null) {
    // Determinar color del marcador según el área
    const area = activity.area_responsable;
    const color = areaColors[area] || '#6c757d';
    
    // Crear icono personalizado
    const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
    
    // Crear marcador
    const marker = L.marker([activity.latitud, activity.longitud], { icon: icon });
    
    // Crear popup con información de la actividad
    const popupContent = createPopupContent(activity);
    marker.bindPopup(popupContent, { maxWidth: 300 });
    
    // Evento de clic en el marcador
    if (clickCallback) {
        marker.on('click', function() {
            clickCallback(activity);
        });
    }
    
    return marker;
}

/**
 * Crear contenido del popup
 * @param {Object} activity - Datos de la actividad
 * @returns {string} HTML del popup
 */
function createPopupContent(activity) {
    const areaText = activity.area_responsable === 'otro' ? 
        (activity.area_otro || 'Otro') : activity.area_responsable;
    
    return `
        <div class="activity-popup">
            <h4>${activity.tipo_actividad}</h4>
            <p><strong>Responsable:</strong> ${activity.nombre_responsable}</p>
            <p><strong>Área:</strong> ${areaText}</p>
            <p><strong>Personas impactadas:</strong> ${activity.personas_impactadas}</p>
            <p><strong>Fecha:</strong> ${formatDate(activity.fecha_creacion)}</p>
            <button class="btn btn-sm btn-primary" onclick="showActivityInfo(${JSON.stringify(activity).replace(/"/g, '&quot;')})">
                Ver más detalles
            </button>
        </div>
    `;
}

/**
 * Inicializar menú lateral
 */
function initializeSideMenu() {
    const menuBtn = document.getElementById('menu-btn');
    const sideMenu = document.getElementById('side-menu');
    const menuOverlay = document.getElementById('menu-overlay');
    
    if (menuBtn && sideMenu && menuOverlay) {
        menuBtn.addEventListener('click', function() {
            sideMenu.classList.toggle('active');
            menuOverlay.classList.toggle('active');
        });
        
        menuOverlay.addEventListener('click', function() {
            sideMenu.classList.remove('active');
            menuOverlay.classList.remove('active');
        });
    }
}

// Inicializar menú lateral cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeSideMenu();
});

// Exportar funciones para uso global
window.addSectoresCatastrales = addSectoresCatastrales;
window.addExampleSectores = addExampleSectores;
window.centerMap = centerMap;
window.formatDate = formatDate;
window.showAlert = showAlert;
window.formatFileSize = formatFileSize;
window.createActivityMarker = createActivityMarker;
window.createPopupContent = createPopupContent;
