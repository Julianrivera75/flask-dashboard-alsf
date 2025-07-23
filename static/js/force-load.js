// Script para forzar la carga de datos y mapas - Versión independiente
console.log('🚀 Iniciando carga forzada de datos y mapas (versión independiente)...');

// Variables globales
let forceLoadMap = null;
let isForceLoadInitialized = false;
let forceLoadLayers = {
    puntosCriticos: null,
    bateriaSocial: null,
    elConsuelo: null
};

// Función para esperar a que el mapa esté disponible
function waitForForceLoadMap() {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 60; // 30 segundos máximo
        
        const checkMap = () => {
            attempts++;
            console.log(`🔄 [Force-Load] Intento ${attempts}/${maxAttempts} de encontrar mapa válido`);
            
            // Verificar que el mapa esté en window.map y sea un objeto válido de Leaflet
            if (typeof window.map !== 'undefined' && window.map && typeof window.map.addLayer === 'function') {
                console.log('🗺️ [Force-Load] Mapa válido encontrado:', window.map);
                forceLoadMap = window.map;
                resolve(forceLoadMap);
            } else {
                console.log('⏳ [Force-Load] Esperando mapa válido...', typeof window.map, window.map);
                
                if (attempts >= maxAttempts) {
                    console.error('❌ [Force-Load] Timeout: No se pudo encontrar un mapa válido después de 30 segundos');
                    reject(new Error('Timeout esperando mapa'));
                    return;
                }
                
                setTimeout(checkMap, 500);
            }
        };
        checkMap();
    });
}

// Función para cargar puntos críticos
function forceLoadPuntosCriticos() {
    console.log('📥 [Force-Load] Cargando puntos críticos...');
    
    if (!forceLoadMap || typeof forceLoadMap.addLayer !== 'function') {
        console.error('❌ [Force-Load] Error: Mapa no disponible para puntos críticos');
        return;
    }
    
    // Remover capa anterior si existe
    if (forceLoadLayers.puntosCriticos && forceLoadMap && typeof forceLoadMap.removeLayer === 'function') {
        forceLoadMap.removeLayer(forceLoadLayers.puntosCriticos);
    }
    
    // Datos hardcodeados de los puntos críticos
    const puntosCriticosData = [
        {name: '1', lat: 4.58012, lng: -74.07175, description: 'Punto crítico 1 - Ordinarios, voluminosos y llantas'},
        {name: '2', lat: 4.57981, lng: -74.07009, description: 'Punto crítico 2 - Ordinarios y escombro'},
        {name: '3', lat: 4.58061, lng: -74.07126, description: 'Punto crítico 3 - Ordinarios y escombro'},
        {name: '6', lat: 4.58111, lng: -74.07056, description: 'Punto crítico 6 - Ordinarios, escombros y llantas'},
        {name: '7', lat: 4.58111, lng: -74.06871, description: 'Punto crítico 7 - Ordinarios y escombro'},
        {name: '8', lat: 4.58131, lng: -74.0683, description: 'Punto crítico 8 - Ordinarios y voluminosos'},
        {name: '9', lat: 4.58224, lng: -74.06815, description: 'Punto crítico 9 - Ordinarios y escombro'},
        {name: '10', lat: 4.58224, lng: -74.06994, description: 'Punto crítico 10 - Ordinarios y voluminosos'},
        {name: '11', lat: 4.58213, lng: -74.06958, description: 'Punto crítico 11 - Ordinarios y escombro'},
        {name: '12', lat: 4.58178, lng: -74.07041, description: 'Punto crítico 12 - Ordinarios y voluminosos'},
        {name: '13', lat: 4.58255, lng: -74.07025, description: 'Punto crítico 13 - Ordinarios y escombro'},
        {name: '14', lat: 4.5836, lng: -74.06959, description: 'Punto crítico 14 - Ordinarios y voluminosos'},
        {name: '15', lat: 4.58163, lng: -74.07131, description: 'Punto crítico 15 - Ordinarios'}
    ];

    console.log('📍 [Force-Load] Datos de puntos críticos cargados:', puntosCriticosData.length, 'puntos');
    
    // Crear marcadores
    const markers = [];
    const latlngs = [];
    
    puntosCriticosData.forEach(punto => {
        const color = ['1', '3', '6', '15'].includes(punto.name) ? 'green' : 'red';
        const iconUrl = color === 'green' 
            ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'
            : 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png';
        
        const marker = L.marker([punto.lat, punto.lng], {
            icon: L.divIcon({
                className: 'custom-marker-' + color,
                html: '<div style="position:relative; width:30px; height:41px;">' +
                      '<img src="' + iconUrl + '" style="position:absolute; left:0; top:0; width:30px; height:41px;">' +
                      '<span style="position:absolute; top:7px; left:0; width:30px; text-align:center; color:black; font-weight:bold; font-size:24px; text-shadow:1px 1px 2px #fff;">' + punto.name + '</span>' +
                      '</div>',
                iconSize: [30, 41],
                iconAnchor: [15, 41],
                popupAnchor: [1, -34]
            })
        });
        
        marker.bindPopup(punto.description);
        markers.push(marker);
        latlngs.push([punto.lat, punto.lng]);
    });
    
    // Agregar al mapa
    if (forceLoadMap && typeof forceLoadMap.addLayer === 'function') {
        const layerGroup = L.layerGroup(markers);
        layerGroup.addTo(forceLoadMap);
        
        if (latlngs.length > 0) {
            forceLoadMap.fitBounds(latlngs, {padding: [50, 50]});
        }
        
        forceLoadLayers.puntosCriticos = layerGroup;
        console.log('✅ [Force-Load] Puntos críticos agregados al mapa:', markers.length, 'marcadores');
    } else {
        console.error('❌ [Force-Load] Error: Mapa no disponible o no tiene método addLayer');
    }
}

// Función para cargar batería social
function forceLoadBateriaSocial() {
    console.log('🔋 [Force-Load] Cargando batería social...');
    
    if (!forceLoadMap || typeof forceLoadMap.addLayer !== 'function') {
        console.error('❌ [Force-Load] Error: Mapa no disponible para batería social');
        return;
    }
    
    // Remover capa anterior si existe
    if (forceLoadLayers.bateriaSocial && forceLoadMap && typeof forceLoadMap.removeLayer === 'function') {
        forceLoadMap.removeLayer(forceLoadLayers.bateriaSocial);
    }
    
    try {
        if (typeof omnivore !== 'undefined') {
            console.log('📄 [Force-Load] Cargando KML de batería social...');
            const bateriaLayer = omnivore.kml('/static/data/Bateria_social.kml')
                .on('ready', function() {
                    console.log('✅ [Force-Load] KML de batería social cargado exitosamente');
                    this.eachLayer(function(layer) {
                        if (layer.setStyle) {
                            layer.setStyle({color: '#4ECDC4', weight: 3, fillOpacity: 0.5});
                        }
                    });
                })
                .on('error', function(error) {
                    console.error('❌ [Force-Load] Error cargando batería social:', error);
                });
            
            if (forceLoadMap && typeof forceLoadMap.addLayer === 'function') {
                bateriaLayer.addTo(forceLoadMap);
                forceLoadLayers.bateriaSocial = bateriaLayer;
                console.log('✅ [Force-Load] Batería social agregada al mapa exitosamente');
            }
        } else {
            console.error('❌ [Force-Load] Error: Omnivore no disponible');
        }
    } catch (error) {
        console.error('❌ [Force-Load] Error en carga de batería social:', error);
    }
}

// Función para remover puntos críticos
function forceRemovePuntosCriticos() {
    console.log('❌ [Force-Load] Removiendo puntos críticos...');
    if (forceLoadLayers.puntosCriticos && forceLoadMap && typeof forceLoadMap.removeLayer === 'function') {
        forceLoadMap.removeLayer(forceLoadLayers.puntosCriticos);
        forceLoadLayers.puntosCriticos = null;
        console.log('✅ [Force-Load] Puntos críticos removidos');
    }
}

// Función para remover batería social
function forceRemoveBateriaSocial() {
    console.log('❌ [Force-Load] Removiendo batería social...');
    if (forceLoadLayers.bateriaSocial && forceLoadMap && typeof forceLoadMap.removeLayer === 'function') {
        forceLoadMap.removeLayer(forceLoadLayers.bateriaSocial);
        forceLoadLayers.bateriaSocial = null;
        console.log('✅ [Force-Load] Batería social removida');
    }
}

// Función para configurar toggles de forma independiente
function setupForceLoadToggles() {
    console.log('🎛️ [Force-Load] Configurando toggles independientes...');
    
    // Función helper para configurar un toggle
    function setupToggle(toggleId, onToggle, offToggle) {
        const toggle = document.getElementById(toggleId);
        if (toggle) {
            console.log(`✅ [Force-Load] Toggle ${toggleId} encontrado`);
            
            // Crear un nuevo listener sin interferir con los existentes
            const originalOnChange = toggle.onchange;
            
            toggle.addEventListener('change', function(e) {
                console.log(`🔄 [Force-Load] Toggle ${toggleId}:`, e.target.checked);
                
                // Ejecutar nuestro código
                if (e.target.checked) {
                    if (onToggle) onToggle();
                } else {
                    if (offToggle) offToggle();
                }
                
                // Ejecutar el código original si existe
                if (originalOnChange) {
                    originalOnChange.call(this, e);
                }
            });
            
            return toggle;
        } else {
            console.error(`❌ [Force-Load] Error: No se encontró el toggle ${toggleId}`);
            return null;
        }
    }
    
    // Toggle puntos críticos
    setupToggle('toggle-puntos-criticos', 
        forceLoadPuntosCriticos,
        forceRemovePuntosCriticos
    );
    
    // Toggle puntos intervenidos (por ahora igual que puntos críticos)
    setupToggle('toggle-puntos-intervenidos',
        forceLoadPuntosCriticos,
        forceRemovePuntosCriticos
    );
    
    // Toggle batería social
    setupToggle('toggle-bateria-social',
        forceLoadBateriaSocial,
        forceRemoveBateriaSocial
    );
}

// Función principal de inicialización
async function initializeForceLoad() {
    if (isForceLoadInitialized) {
        console.log('⚠️ [Force-Load] Ya inicializado, saltando...');
        return;
    }
    
    console.log('🚀 [Force-Load] Inicializando carga forzada...');
    
    try {
        // Esperar a que el mapa esté disponible
        await waitForForceLoadMap();
        console.log('✅ [Force-Load] Mapa disponible, configurando...');
        
        // Configurar toggles
        setupForceLoadToggles();
        
        isForceLoadInitialized = true;
        console.log('✅ [Force-Load] Inicialización completada exitosamente');
        
    } catch (error) {
        console.error('❌ [Force-Load] Error en inicialización:', error);
        // Intentar configurar toggles de todas formas
        setupForceLoadToggles();
    }
}

// Función para verificar si el DOM está listo
function isDOMReady() {
    return document.readyState === 'complete' || document.readyState === 'interactive';
}

// Función para esperar a que el DOM esté listo
function waitForDOM() {
    return new Promise((resolve) => {
        if (isDOMReady()) {
            resolve();
        } else {
            document.addEventListener('DOMContentLoaded', resolve);
            window.addEventListener('load', resolve);
        }
    });
}

// Inicialización principal
async function main() {
    console.log('🚀 [Force-Load] Iniciando script force-load...');
    
    try {
        // Esperar a que el DOM esté listo
        await waitForDOM();
        console.log('✅ [Force-Load] DOM listo');
        
        // Esperar un poco más para asegurar que todos los scripts estén cargados
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Inicializar
        await initializeForceLoad();
        
    } catch (error) {
        console.error('❌ [Force-Load] Error en inicialización principal:', error);
    }
}

// Ejecutar inicialización
main();

console.log('🚀 [Force-Load] Script de carga forzada inicializado'); 