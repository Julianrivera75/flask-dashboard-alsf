/**
 * JavaScript para la página de listar actividades de 1000 Acciones en 1 Día
 */

// Variables globales
let dataTable;
let activitiesData = [];

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeDataTable();
    loadActivities();
    setupFilters();
    setupMenu();
    updateStats();
});

/**
 * Inicializar DataTable
 */
function initializeDataTable() {
    const table = document.getElementById('actividades-table');
    
    if (table) {
        dataTable = $('#actividades-table').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
            },
            pageLength: 25,
            order: [[0, 'desc']], // Ordenar por ID descendente
            columnDefs: [
                {
                    targets: [0], // Columna ID
                    width: '60px'
                },
                {
                    targets: [1], // Columna Responsable
                    width: '150px'
                },
                {
                    targets: [2], // Columna Tipo de Actividad
                    width: '200px'
                },
                {
                    targets: [3], // Columna Área
                    width: '120px'
                },
                {
                    targets: [4], // Columna Personas Impactadas
                    width: '120px',
                    className: 'text-center'
                },
                {
                    targets: [5], // Columna Fecha
                    width: '120px'
                },
                {
                    targets: [6, 7, 8], // Columnas de acciones
                    width: '100px',
                    className: 'text-center',
                    orderable: false
                }
            ],
            dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
                 '<"row"<"col-sm-12"tr>>' +
                 '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
            lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]]
        });
    }
}

/**
 * Cargar actividades desde la API
 */
function loadActivities() {
    fetch('/acciones-1000/api/actividades')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                activitiesData = data.actividades;
                updateStats();
            } else {
                showAlert('Error', 'Error al cargar las actividades', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error', 'Error de conexión al cargar actividades', 'error');
        });
}

/**
 * Configurar filtros
 */
function setupFilters() {
    const filterArea = document.getElementById('filter-area');
    const filterTipo = document.getElementById('filter-tipo');
    const filterFecha = document.getElementById('filter-fecha');
    
    if (filterArea) {
        filterArea.addEventListener('change', applyFilters);
    }
    
    if (filterTipo) {
        filterTipo.addEventListener('change', applyFilters);
    }
    
    if (filterFecha) {
        filterFecha.addEventListener('change', applyFilters);
    }
}

/**
 * Aplicar filtros
 */
function applyFilters() {
    const filterArea = document.getElementById('filter-area');
    const filterTipo = document.getElementById('filter-tipo');
    const filterFecha = document.getElementById('filter-fecha');
    
    if (dataTable) {
        // Limpiar filtros previos
        dataTable.search('').columns().search('').draw();
        
        // Aplicar filtros
        if (filterArea && filterArea.value) {
            dataTable.column(3).search(filterArea.value).draw();
        }
        
        if (filterTipo && filterTipo.value) {
            dataTable.column(2).search(filterTipo.value).draw();
        }
        
        if (filterFecha && filterFecha.value) {
            // Filtrar por fecha en la columna de fecha
            const filterDate = new Date(filterFecha.value);
            const filterDateStr = filterDate.toLocaleDateString('es-ES');
            
            dataTable.column(5).search(filterDateStr).draw();
        }
    }
}

/**
 * Limpiar filtros
 */
function clearFilters() {
    const filterArea = document.getElementById('filter-area');
    const filterTipo = document.getElementById('filter-tipo');
    const filterFecha = document.getElementById('filter-fecha');
    
    if (filterArea) filterArea.value = '';
    if (filterTipo) filterTipo.value = '';
    if (filterFecha) filterFecha.value = '';
    
    if (dataTable) {
        dataTable.search('').columns().search('').draw();
    }
}

/**
 * Actualizar estadísticas
 */
function updateStats() {
    if (activitiesData.length === 0) return;
    
    // Total de actividades
    const totalActividades = document.getElementById('total-actividades');
    if (totalActividades) {
        totalActividades.textContent = activitiesData.length;
    }
    
    // Total de personas impactadas
    const totalPersonas = document.getElementById('total-personas');
    if (totalPersonas) {
        const totalImpact = activitiesData.reduce((sum, activity) => sum + activity.personas_impactadas, 0);
        totalPersonas.textContent = totalImpact.toLocaleString();
    }
    
    // Actividades de hoy
    const actividadesHoy = document.getElementById('actividades-hoy');
    if (actividadesHoy) {
        const today = new Date().toDateString();
        const todayActivities = activitiesData.filter(activity => 
            new Date(activity.fecha_creacion).toDateString() === today
        );
        actividadesHoy.textContent = todayActivities.length;
    }
    
    // Áreas activas
    const areasActivas = document.getElementById('areas-activas');
    if (areasActivas) {
        const areas = new Set(activitiesData.map(activity => activity.area_responsable));
        areasActivas.textContent = areas.size;
    }
}

/**
 * Ver detalles de una actividad
 */
function viewActivity(activityId) {
    const activity = activitiesData.find(a => a.id === activityId);
    
    if (!activity) {
        showAlert('Error', 'Actividad no encontrada', 'error');
        return;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('activityModal'));
    const modalBody = document.getElementById('activityModalBody');
    
    if (modalBody) {
        const areaText = activity.area_responsable === 'otro' ? 
            (activity.area_otro || 'Otro') : activity.area_responsable;
        
        modalBody.innerHTML = `
            <div class="activity-details-modal">
                <div class="detail-section">
                    <h6>Información General</h6>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <label>ID:</label>
                            <span>${activity.id}</span>
                        </div>
                        <div class="detail-item">
                            <label>Responsable:</label>
                            <span>${activity.nombre_responsable}</span>
                        </div>
                        <div class="detail-item">
                            <label>Tipo de Actividad:</label>
                            <span>${activity.tipo_actividad}</span>
                        </div>
                        <div class="detail-item">
                            <label>Área:</label>
                            <span>${areaText}</span>
                        </div>
                        <div class="detail-item">
                            <label>Personas Impactadas:</label>
                            <span>${activity.personas_impactadas}</span>
                        </div>
                        <div class="detail-item">
                            <label>Fecha de Registro:</label>
                            <span>${formatDate(activity.fecha_creacion)}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h6>Descripción</h6>
                    <p>${activity.descripcion_detallada}</p>
                </div>
                
                ${activity.observaciones_adicionales ? `
                <div class="detail-section">
                    <h6>Observaciones Adicionales</h6>
                    <p>${activity.observaciones_adicionales}</p>
                </div>
                ` : ''}
                
                <div class="detail-section">
                    <h6>Ubicación</h6>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <label>Latitud:</label>
                            <span>${activity.latitud}</span>
                        </div>
                        <div class="detail-item">
                            <label>Longitud:</label>
                            <span>${activity.longitud}</span>
                        </div>
                    </div>
                    <button type="button" class="btn btn-sm btn-info mt-2" onclick="showLocation(${activity.latitud}, ${activity.longitud})">
                        <i class="fas fa-map-marker-alt"></i> Ver en Mapa
                    </button>
                </div>
                
                <div class="detail-section">
                    <h6>Fotos</h6>
                    ${activity.fotos && activity.fotos.length > 0 ? 
                        `<p>La actividad tiene ${activity.fotos.length} foto(s) registrada(s).</p>
                         <button type="button" class="btn btn-sm btn-primary" onclick="viewPhotos(${activity.id})">
                             <i class="fas fa-images"></i> Ver Fotos
                         </button>` : 
                        '<p>No hay fotos registradas para esta actividad.</p>'
                    }
                </div>
            </div>
        `;
    }
    
    modal.show();
}

/**
 * Ver fotos de una actividad
 */
function viewPhotos(activityId) {
    const activity = activitiesData.find(a => a.id === activityId);
    
    if (!activity) {
        showAlert('Error', 'Actividad no encontrada', 'error');
        return;
    }
    
    if (!activity.fotos || activity.fotos.length === 0) {
        showAlert('Información', 'Esta actividad no tiene fotos registradas', 'info');
        return;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('photosModal'));
    const modalBody = document.getElementById('photosModalBody');
    
    if (modalBody) {
        let photosHtml = '<div class="photos-gallery">';
        
        activity.fotos.forEach(photo => {
            photosHtml += `
                <div class="photo-item">
                    <img src="/${photo.ruta_archivo}" alt="Foto de la actividad" class="img-fluid">
                    <div class="photo-info">
                        <small>${photo.nombre_original}</small>
                        <br>
                        <small class="text-muted">${formatFileSize(photo.tamano_bytes)}</small>
                    </div>
                </div>
            `;
        });
        
        photosHtml += '</div>';
        modalBody.innerHTML = photosHtml;
    }
    
    modal.show();
}

/**
 * Mostrar ubicación en el mapa
 */
function showLocation(lat, lng) {
    // Abrir el mapa en una nueva pestaña o redirigir
    const mapUrl = `/acciones-1000/mapa?lat=${lat}&lng=${lng}`;
    window.open(mapUrl, '_blank');
}

/**
 * Exportar datos
 */
function exportData() {
    if (activitiesData.length === 0) {
        showAlert('Información', 'No hay datos para exportar', 'info');
        return;
    }
    
    // Preparar datos para exportación
    const exportData = activitiesData.map(activity => ({
        ID: activity.id,
        'Tipo de Actividad': activity.tipo_actividad,
        'Responsable': activity.nombre_responsable,
        'Área': activity.area_responsable === 'otro' ? (activity.area_otro || 'Otro') : activity.area_responsable,
        'Personas Impactadas': activity.personas_impactadas,
        'Descripción': activity.descripcion_detallada,
        'Observaciones': activity.observaciones_adicionales || '',
        'Latitud': activity.latitud,
        'Longitud': activity.longitud,
        'Fecha de Registro': formatDate(activity.fecha_creacion),
        'Fotos': activity.fotos ? activity.fotos.length : 0
    }));
    
    // Crear CSV
    const csvContent = convertToCSV(exportData);
    downloadCSV(csvContent, 'actividades_1000_acciones.csv');
}

/**
 * Convertir datos a CSV
 */
function convertToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];
    
    for (const row of data) {
        const values = headers.map(header => {
            const value = row[header];
            // Escapar comillas y envolver en comillas si contiene comas
            const escapedValue = String(value).replace(/"/g, '""');
            return `"${escapedValue}"`;
        });
        csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
}

/**
 * Descargar archivo CSV
 */
function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showAlert('Éxito', 'Datos exportados correctamente', 'success');
    }
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Formatear tamaño de archivo
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Mostrar alerta
 */
function showAlert(title, message, type = 'info') {
    Swal.fire({
        title: title,
        text: message,
        icon: type,
        confirmButtonColor: '#e4032e',
        confirmButtonText: 'Aceptar'
    });
}

/**
 * Configurar menú lateral
 */
function setupMenu() {
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

// Exportar funciones para uso global
window.clearFilters = clearFilters;
window.exportData = exportData;
window.viewActivity = viewActivity;
window.viewPhotos = viewPhotos;
window.showLocation = showLocation;
