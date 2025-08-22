from flask import Blueprint, jsonify, request, render_template
from services.analytics_service import AnalyticsService
from datetime import datetime
import time

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')
analytics_service = AnalyticsService()

@analytics_bp.route('/dashboard')
def dashboard():
    """Dashboard principal de analytics"""
    return render_template('analytics_dashboard.html')

@analytics_bp.route('/api/stats')
def get_stats():
    """API para obtener estadísticas de tráfico"""
    try:
        days = request.args.get('days', 30, type=int)
        stats = analytics_service.get_traffic_stats(days)
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analytics_bp.route('/api/realtime')
def get_realtime_stats():
    """API para obtener estadísticas en tiempo real"""
    try:
        stats = analytics_service.get_realtime_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analytics_bp.route('/api/track', methods=['POST'])
def track_event():
    """API para tracking de eventos personalizados"""
    try:
        data = request.get_json()
        event_type = data.get('event_type')
        event_data = data.get('event_data', {})
        
        if not event_type:
            return jsonify({
                'success': False,
                'error': 'event_type es requerido'
            }), 400
        
        success = analytics_service.track_user_event(event_type, event_data)
        
        return jsonify({
            'success': success,
            'message': 'Evento registrado exitosamente' if success else 'Error al registrar evento'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analytics_bp.route('/api/export/<format>')
def export_data(format):
    """API para exportar datos de analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        
        if format not in ['csv', 'json']:
            return jsonify({
                'success': False,
                'error': 'Formato no soportado. Use csv o json'
            }), 400
        
        # Aquí implementarías la lógica de exportación
        # Por ahora retornamos un mensaje de placeholder
        
        return jsonify({
            'success': True,
            'message': f'Exportación en formato {format} para {days} días',
            'note': 'Funcionalidad de exportación en desarrollo'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analytics_bp.route('/api/health')
def health_check():
    """Health check para el sistema de analytics"""
    try:
        # Verificar que el servicio esté funcionando
        test_stats = analytics_service.get_traffic_stats(1)
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'analytics',
            'test_data': len(test_stats) > 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
