import time
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import request, session
from sqlalchemy import func, desc
from models.analytics import PageView, UserEvent, TrafficSummary
from models import db

class AnalyticsService:
    """Servicio para tracking y análisis de tráfico web"""
    
    def __init__(self):
        self.db = db
    
    def track_page_view(self, page_url: str, load_time: Optional[int] = None) -> bool:
        """Registrar una vista de página"""
        try:
            # Obtener información del request
            user_agent = request.headers.get('User-Agent', '')
            ip_address = self._get_client_ip()
            referrer = request.headers.get('Referer', '')
            session_id = session.get('session_id', self._generate_session_id())
            
            # Crear registro de vista
            page_view = PageView(
                page_url=page_url,
                user_agent=user_agent,
                ip_address=ip_address,
                referrer=referrer,
                session_id=session_id,
                load_time=load_time,
                user_id=session.get('user_id')
            )
            
            self.db.session.add(page_view)
            self.db.session.commit()
            
            # Actualizar resumen diario
            self._update_daily_summary()
            
            return True
            
        except Exception as e:
            print(f"Error tracking page view: {e}")
            self.db.session.rollback()
            return False
    
    def track_user_event(self, event_type: str, event_data: Dict = None) -> bool:
        """Registrar un evento de usuario"""
        try:
            user_event = UserEvent(
                event_type=event_type,
                event_data=event_data or {},
                page_url=request.url,
                user_agent=request.headers.get('User-Agent', ''),
                ip_address=self._get_client_ip(),
                session_id=session.get('session_id', self._generate_session_id()),
                user_id=session.get('user_id')
            )
            
            self.db.session.add(user_event)
            self.db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"Error tracking user event: {e}")
            self.db.session.rollback()
            return False
    
    def get_traffic_stats(self, days: int = 30) -> Dict:
        """Obtener estadísticas de tráfico"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Vistas totales
            total_views = PageView.query.filter(
                PageView.timestamp >= start_date
            ).count()
            
            # Visitantes únicos (por IP)
            unique_visitors = db.session.query(
                func.count(func.distinct(PageView.ip_address))
            ).filter(
                PageView.timestamp >= start_date
            ).scalar()
            
            # Sesiones únicas
            unique_sessions = db.session.query(
                func.count(func.distinct(PageView.session_id))
            ).filter(
                PageView.timestamp >= start_date
            ).scalar()
            
            # Páginas más visitadas
            top_pages = db.session.query(
                PageView.page_url,
                func.count(PageView.id).label('views')
            ).filter(
                PageView.timestamp >= start_date
            ).group_by(PageView.page_url).order_by(
                desc('views')
            ).limit(10).all()
            
            # Tiempo promedio de carga
            avg_load_time = db.session.query(
                func.avg(PageView.load_time)
            ).filter(
                PageView.timestamp >= start_date,
                PageView.load_time.isnot(None)
            ).scalar() or 0
            
            return {
                'total_views': total_views,
                'unique_visitors': unique_visitors,
                'unique_sessions': unique_sessions,
                'avg_load_time': round(avg_load_time, 2),
                'top_pages': [{'url': page, 'views': views} for page, views in top_pages],
                'period_days': days
            }
            
        except Exception as e:
            print(f"Error getting traffic stats: {e}")
            return {}
    
    def get_realtime_stats(self) -> Dict:
        """Obtener estadísticas en tiempo real (últimas 24 horas)"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(hours=24)
            
            # Vistas en las últimas 24 horas
            views_24h = PageView.query.filter(
                PageView.timestamp >= start_date
            ).count()
            
            # Visitantes únicos en las últimas 24 horas
            visitors_24h = db.session.query(
                func.count(func.distinct(PageView.ip_address))
            ).filter(
                PageView.timestamp >= start_date
            ).scalar()
            
            # Vistas por hora (últimas 24 horas)
            hourly_views = db.session.query(
                func.date_trunc('hour', PageView.timestamp).label('hour'),
                func.count(PageView.id).label('views')
            ).filter(
                PageView.timestamp >= start_date
            ).group_by('hour').order_by('hour').all()
            
            return {
                'views_24h': views_24h,
                'visitors_24h': visitors_24h,
                'hourly_views': [{'hour': str(hour), 'views': views} for hour, views in hourly_views]
            }
            
        except Exception as e:
            print(f"Error getting realtime stats: {e}")
            return {}
    
    def _get_client_ip(self) -> str:
        """Obtener IP del cliente considerando proxies"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    def _generate_session_id(self) -> str:
        """Generar ID de sesión único"""
        if 'session_id' not in session:
            session['session_id'] = hashlib.md5(
                f"{self._get_client_ip()}{time.time()}".encode()
            ).hexdigest()
        return session['session_id']
    
    def _update_daily_summary(self):
        """Actualizar resumen diario de tráfico"""
        try:
            today = datetime.utcnow().date()
            
            # Verificar si ya existe un resumen para hoy
            summary = TrafficSummary.query.filter(
                func.date(TrafficSummary.date) == today
            ).first()
            
            if not summary:
                summary = TrafficSummary(date=datetime.utcnow())
                self.db.session.add(summary)
            
            # Actualizar estadísticas
            summary.total_views = PageView.query.filter(
                func.date(PageView.timestamp) == today
            ).count()
            
            summary.unique_visitors = db.session.query(
                func.count(func.distinct(PageView.ip_address))
            ).filter(
                func.date(PageView.timestamp) == today
            ).scalar()
            
            summary.total_sessions = db.session.query(
                func.count(func.distinct(PageView.session_id))
            ).filter(
                func.date(PageView.timestamp) == today
            ).scalar()
            
            # Top páginas del día
            top_pages = db.session.query(
                PageView.page_url,
                func.count(PageView.id).label('views')
            ).filter(
                func.date(PageView.timestamp) == today
            ).group_by(PageView.page_url).order_by(
                desc('views')
            ).limit(5).all()
            
            summary.top_pages = [{'url': page, 'views': views} for page, views in top_pages]
            
            self.db.session.commit()
            
        except Exception as e:
            print(f"Error updating daily summary: {e}")
            self.db.session.rollback()
