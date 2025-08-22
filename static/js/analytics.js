/**
 * Sistema de Analytics para el Frontend
 * Tracking automático de eventos de usuario
 */

class AnalyticsTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.init();
    }
    
    init() {
        // Tracking automático de eventos
        this.trackPageView();
        this.trackClicks();
        this.trackFormSubmissions();
        this.trackNavigation();
        this.trackPerformance();
    }
    
    generateSessionId() {
        // Generar ID de sesión único
        if (!sessionStorage.getItem('analytics_session_id')) {
            const sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('analytics_session_id', sessionId);
        }
        return sessionStorage.getItem('analytics_session_id');
    }
    
    trackPageView() {
        // Tracking de vista de página
        const pageData = {
            url: window.location.href,
            title: document.title,
            referrer: document.referrer,
            timestamp: new Date().toISOString()
        };
        
        this.sendEvent('page_view', pageData);
    }
    
    trackClicks() {
        // Tracking de clicks en elementos importantes
        document.addEventListener('click', (event) => {
            const target = event.target;
            
            // Solo trackear clicks en elementos interactivos
            if (target.tagName === 'A' || target.tagName === 'BUTTON' || 
                target.closest('a') || target.closest('button')) {
                
                const clickData = {
                    element: target.tagName.toLowerCase(),
                    text: target.textContent?.trim() || target.alt || 'Unknown',
                    href: target.href || target.closest('a')?.href || '',
                    class: target.className || '',
                    id: target.id || ''
                };
                
                this.sendEvent('click', clickData);
            }
        });
    }
    
    trackFormSubmissions() {
        // Tracking de envíos de formularios
        document.addEventListener('submit', (event) => {
            const form = event.target;
            const formData = {
                action: form.action,
                method: form.method,
                form_id: form.id || 'unknown',
                form_class: form.className || '',
                field_count: form.elements.length
            };
            
            this.sendEvent('form_submit', formData);
        });
    }
    
    trackNavigation() {
        // Tracking de navegación
        let lastUrl = location.href;
        
        // Observar cambios en la URL (SPA navigation)
        const observer = new MutationObserver(() => {
            if (location.href !== lastUrl) {
                lastUrl = location.href;
                this.trackPageView();
            }
        });
        
        observer.observe(document, { subtree: true, childList: true });
        
        // Tracking de navegación con botones del navegador
        window.addEventListener('popstate', () => {
            this.trackPageView();
        });
    }
    
    trackPerformance() {
        // Tracking de rendimiento de la página
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                    
                    const performanceData = {
                        load_time: Math.round(loadTime),
                        dom_content_loaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                        first_paint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
                        first_contentful_paint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
                    };
                    
                    this.sendEvent('performance', performanceData);
                }, 1000);
            });
        }
    }
    
    async sendEvent(eventType, eventData) {
        try {
            const payload = {
                event_type: eventType,
                event_data: {
                    ...eventData,
                    session_id: this.sessionId,
                    user_agent: navigator.userAgent,
                    timestamp: new Date().toISOString(),
                    url: window.location.href
                }
            };
            
            // Enviar evento al backend
            const response = await fetch('/analytics/api/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                console.warn('Analytics event not tracked:', response.status);
            }
            
        } catch (error) {
            // No fallar la aplicación si hay error en analytics
            console.warn('Analytics error:', error);
        }
    }
    
    // Método para tracking manual de eventos
    trackCustomEvent(eventName, data = {}) {
        this.sendEvent(eventName, data);
    }
    
    // Método para tracking de conversiones
    trackConversion(conversionType, value = null) {
        const conversionData = {
            type: conversionType,
            value: value,
            currency: 'COP'
        };
        
        this.sendEvent('conversion', conversionData);
    }
}

// Inicializar analytics cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.analytics = new AnalyticsTracker();
    
    // Exponer métodos globales para uso manual
    window.trackEvent = (eventName, data) => {
        window.analytics.trackCustomEvent(eventName, data);
    };
    
    window.trackConversion = (type, value) => {
        window.analytics.trackConversion(type, value);
    };
    
    console.log('📊 Analytics inicializado');
});

// Tracking de eventos específicos de la aplicación
document.addEventListener('DOMContentLoaded', () => {
    // Tracking de acceso a secciones específicas
    const trackSectionAccess = () => {
        const currentPath = window.location.pathname;
        
        if (currentPath.includes('/el-consuelo')) {
            window.trackEvent('section_access', { section: 'el_consuelo' });
        } else if (currentPath.includes('/san-bernardo')) {
            window.trackEvent('section_access', { section: 'san_bernardo' });
        } else if (currentPath.includes('/formulario-reporte')) {
            window.trackEvent('section_access', { section: 'formulario_reporte' });
        } else if (currentPath.includes('/mapa-reportes')) {
            window.trackEvent('section_access', { section: 'mapa_reportes' });
        }
    };
    
    trackSectionAccess();
});
