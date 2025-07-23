// Script para forzar la carga de datos y mapas
console.log('🚀 Iniciando carga forzada de datos y mapas...');

// Variable global para el mapa
let map = null;

// Función para esperar a que el mapa esté disponible
function waitForMap() {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 60; // 30 segundos máximo (60 * 500ms)
        
        const checkMap = () => {
            attempts++;
            console.log(`🔄 Intento ${attempts}/${maxAttempts} de encontrar mapa válido`);
            
            // Verificar que el mapa esté en window.map y sea un objeto válido de Leaflet
            if (typeof window.map !== 'undefined' && window.map && typeof window.map.addLayer === 'function') {
                console.log('🗺️ Mapa válido encontrado:', window.map);
                map = window.map;
                resolve(map);
            } else {
                console.log('⏳ Esperando mapa válido...', typeof window.map, window.map);
                // Verificar si hay un elemento de mapa en el DOM
                const mapElement = document.getElementById('map');
                if (mapElement) {
                    console.log('📍 Elemento de mapa encontrado en DOM:', mapElement);
                    // Verificar si Leaflet está disponible
                    if (typeof L !== 'undefined') {
                        console.log('🍃 Leaflet disponible:', L);
                    } else {
                        console.log('❌ Leaflet no está disponible');
                    }
                } else {
                    console.log('❌ No se encontró elemento de mapa en DOM');
                }
                
                if (attempts >= maxAttempts) {
                    console.error('❌ Timeout: No se pudo encontrar un mapa válido después de 30 segundos');
                    reject(new Error('Timeout esperando mapa'));
                    return;
                }
                
                setTimeout(checkMap, 500); // Aumentar el intervalo a 500ms
            }
        };
        checkMap();
    });
}

// Función para cargar puntos críticos directamente
function forceLoadPuntosCriticos() {
    console.log('📥 Cargando puntos críticos forzadamente...');
    
    if (!map || typeof map.addLayer !== 'function') {
        console.error('❌ Error: Mapa no disponible o no válido para puntos críticos');
        return;
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

    console.log('📍 Datos de puntos críticos cargados:', puntosCriticosData.length, 'puntos');
    
    // Crear marcadores directamente
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
    if (map && typeof map.addLayer === 'function') {
        const layerGroup = L.layerGroup(markers);
        layerGroup.addTo(map);
        
        if (latlngs.length > 0) {
            map.fitBounds(latlngs, {padding: [50, 50]});
        }
        
        console.log('✅ Puntos críticos agregados al mapa:', markers.length, 'marcadores');
        
        // Guardar referencia para poder remover después
        window.puntosCriticosLayer = layerGroup;
    } else {
        console.error('❌ Error: Mapa no disponible o no tiene método addLayer');
    }
}

// Función para cargar mapa de El Consuelo
function forceLoadElConsuelo() {
    console.log('🗺️ Cargando mapa de El Consuelo forzadamente...');
    
    if (!map || typeof map.addLayer !== 'function') {
        console.error('❌ Error: Mapa no disponible o no válido para El Consuelo');
        return;
    }
    
    if (typeof omnivore !== 'undefined') {
        try {
            console.log('🔍 Verificando mapa antes de cargar KML:', map);
            console.log('🔍 Métodos del mapa:', Object.getOwnPropertyNames(map));
            
            const kmlLayer = omnivore.kml('/static/data/ELCONSUELO.kml')
                .on('ready', function() {
                    console.log('✅ Mapa de El Consuelo cargado correctamente');
                    if (map && typeof map.fitBounds === 'function') {
                        map.fitBounds(this.getBounds());
                    }
                })
                .on('error', function(error) {
                    console.error('❌ Error cargando mapa de El Consuelo:', error);
                });
            
            // Agregar al mapa de forma segura
            if (map && typeof map.addLayer === 'function') {
                kmlLayer.addTo(map);
                window.elConsueloLayer = kmlLayer;
                console.log('✅ KML agregado al mapa exitosamente');
            } else {
                console.error('❌ Error: Mapa no tiene método addLayer');
            }
        } catch (error) {
            console.error('❌ Error en carga de mapa de El Consuelo:', error);
        }
    } else {
        console.error('❌ Error: Omnivore no disponible');
    }
}

// Función para cargar batería social
function forceLoadBateriaSocial() {
    console.log('🔋 Cargando batería social forzadamente...');
    
    if (!map || typeof map.addLayer !== 'function') {
        console.error('❌ Error: Mapa no disponible o no válido para batería social');
        return;
    }
    
    if (typeof omnivore !== 'undefined') {
        try {
            const bateriaLayer = omnivore.kml('/static/data/Bateria_social.kml')
                .on('ready', function() {
                    console.log('✅ Batería social cargada correctamente');
                    this.eachLayer(function(layer) {
                        if (layer.setStyle) {
                            layer.setStyle({color: '#4ECDC4', weight: 3, fillOpacity: 0.5});
                        }
                    });
                })
                .on('error', function(error) {
                    console.error('❌ Error cargando batería social:', error);
                });
            
            // Agregar al mapa de forma segura
            if (map && typeof map.addLayer === 'function') {
                bateriaLayer.addTo(map);
                window.bateriaSocialLayer = bateriaLayer;
                console.log('✅ Batería social agregada al mapa exitosamente');
            } else {
                console.error('❌ Error: Mapa no tiene método addLayer');
            }
        } catch (error) {
            console.error('❌ Error en carga de batería social:', error);
        }
    } else {
        console.error('❌ Error: Omnivore no disponible');
    }
}

// Función para configurar toggles
function setupToggles() {
    console.log('🎛️ Configurando toggles...');
    
    // Toggle puntos críticos
    const togglePuntosCriticos = document.getElementById('toggle-puntos-criticos');
    if (togglePuntosCriticos) {
        togglePuntosCriticos.addEventListener('change', function(e) {
            console.log('🔄 Toggle puntos críticos:', e.target.checked);
            if (e.target.checked) {
                forceLoadPuntosCriticos();
            } else {
                if (window.puntosCriticosLayer && map && typeof map.removeLayer === 'function') {
                    map.removeLayer(window.puntosCriticosLayer);
                    console.log('❌ Puntos críticos removidos');
                }
            }
        });
    }
    
    // Toggle puntos intervenidos
    const togglePuntosIntervenidos = document.getElementById('toggle-puntos-intervenidos');
    if (togglePuntosIntervenidos) {
        togglePuntosIntervenidos.addEventListener('change', function(e) {
            console.log('🔄 Toggle puntos intervenidos:', e.target.checked);
            // Por ahora solo recargamos todos los puntos
            if (e.target.checked) {
                forceLoadPuntosCriticos();
            }
        });
    }
    
    // Toggle batería social
    const toggleBateriaSocial = document.getElementById('toggle-bateria-social');
    if (toggleBateriaSocial) {
        toggleBateriaSocial.addEventListener('change', function(e) {
            console.log('🔄 Toggle batería social:', e.target.checked);
            if (e.target.checked) {
                forceLoadBateriaSocial();
            } else {
                if (window.bateriaSocialLayer && map && typeof map.removeLayer === 'function') {
                    map.removeLayer(window.bateriaSocialLayer);
                    console.log('❌ Batería social removida');
                }
            }
        });
    }
}

// Función principal de inicialización
async function initializeForceLoad() {
    console.log('🚀 Inicializando carga forzada...');
    
    try {
        // Esperar a que el mapa esté disponible
        await waitForMap();
        console.log('✅ Mapa disponible, configurando...');
        
        // Configurar toggles
        setupToggles();
        
        // Cargar mapa de El Consuelo automáticamente
        setTimeout(forceLoadElConsuelo, 500);
        
    } catch (error) {
        console.error('❌ Error en inicialización:', error);
    }
}

// Ejecutar inicialización inmediatamente ya que el script se carga al final
initializeForceLoad();

console.log('🚀 Script de carga forzada inicializado'); 