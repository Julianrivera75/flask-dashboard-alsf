from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PageView(Base):
    """Modelo para tracking de vistas de página"""
    __tablename__ = 'page_views'
    
    id = Column(Integer, primary_key=True)
    page_url = Column(String(500), nullable=False)
    user_agent = Column(Text)
    ip_address = Column(String(45))  # IPv6 compatible
    referrer = Column(String(500))
    session_id = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    load_time = Column(Integer)  # Tiempo de carga en ms
    user_id = Column(Integer, nullable=True)  # Si el usuario está autenticado
    
    def __repr__(self):
        return f'<PageView {self.page_url} at {self.timestamp}>'

class UserEvent(Base):
    """Modelo para tracking de eventos de usuario"""
    __tablename__ = 'user_events'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)  # click, form_submit, etc.
    event_data = Column(JSON)  # Datos adicionales del evento
    page_url = Column(String(500))
    user_agent = Column(Text)
    ip_address = Column(String(45))
    session_id = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f'<UserEvent {self.event_type} at {self.timestamp}>'

class TrafficSummary(Base):
    """Modelo para resúmenes diarios de tráfico"""
    __tablename__ = 'traffic_summary'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    total_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    avg_load_time = Column(Integer, default=0)
    top_pages = Column(JSON)  # Páginas más visitadas
    top_referrers = Column(JSON)  # Referrers principales
    
    def __repr__(self):
        return f'<TrafficSummary {self.date}: {self.total_views} views>'
