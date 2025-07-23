// Script para deshabilitar Lightbox y prevenir errores
console.log('🔧 Inicializando fix para Lightbox...');

// Deshabilitar Lightbox completamente
window.lightbox = {
    start: function() { console.log('🚫 Lightbox deshabilitado'); },
    end: function() { console.log('🚫 Lightbox deshabilitado'); }
};

// Prevenir que se ejecute cualquier función de Lightbox
if (typeof window.lightbox !== 'undefined') {
    console.log('🚫 Lightbox detectado, deshabilitando...');
    window.lightbox = {
        start: function() { return false; },
        end: function() { return false; },
        init: function() { return false; }
    };
}

// Interceptar cualquier llamada a funciones de Lightbox
const originalQuerySelector = document.querySelector;
document.querySelector = function(selector) {
    if (selector && selector.includes('lightbox')) {
        console.log('🚫 Interceptando selector de Lightbox:', selector);
        return null;
    }
    return originalQuerySelector.call(this, selector);
};

// Prevenir errores de Lightbox en popups
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM cargado, aplicando fixes...');
    
    // Remover cualquier script de Lightbox
    const lightboxScripts = document.querySelectorAll('script[src*="lightbox"]');
    lightboxScripts.forEach(script => {
        console.log('🚫 Removiendo script de Lightbox:', script.src);
        script.remove();
    });
    
    // Remover cualquier enlace de Lightbox
    const lightboxLinks = document.querySelectorAll('a[data-lightbox]');
    lightboxLinks.forEach(link => {
        console.log('🚫 Removiendo enlace de Lightbox:', link.href);
        link.removeAttribute('data-lightbox');
        link.onclick = function(e) {
            e.preventDefault();
            console.log('🚫 Click en enlace de Lightbox prevenido');
        };
    });
    
    console.log('✅ Fixes aplicados correctamente');
});

// Función para forzar la carga del KML
function forceKMLReload() {
    console.log('🔄 Forzando recarga del KML...');
    
    // Simular un click en el toggle para recargar
    const toggle = document.getElementById('toggle-puntos-criticos');
    if (toggle) {
        console.log('🎯 Toggle encontrado, forzando recarga...');
        toggle.checked = false;
        setTimeout(() => {
            toggle.checked = true;
            toggle.dispatchEvent(new Event('change'));
            console.log('✅ KML recargado forzadamente');
        }, 100);
    } else {
        console.error('❌ Toggle no encontrado');
    }
}

// Ejecutar después de 2 segundos para asegurar que todo esté cargado
setTimeout(forceKMLReload, 2000);

console.log('🔧 Fix para Lightbox inicializado correctamente'); 