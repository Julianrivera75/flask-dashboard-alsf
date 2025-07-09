import plotly.graph_objects as go
import plotly.express as px
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from config.development import DevelopmentConfig

class ChartGenerator:
    """
    Clase para generar gráficos y visualizaciones de datos
    """
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        # Usar configuración del archivo config.py original
        self.colors = {
            'marzo': '#FF6B6B',
            'abril': '#4ECDC4', 
            'mayo': '#45B7D1',
            'junio': '#96CEB4',
            'julio': '#FFEAA7',
            'agosto': '#DDA0DD',
            'septiembre': '#98D8C8',
            'octubre': '#F7DC6F',
            'noviembre': '#BB8FCE',
            'diciembre': '#85C1E9',
            'alcaldia': '#FF6B6B',  # Rojo para Alcaldía
            'default': '#4ECDC4'    # Verde por defecto
        }
        
        self.important_columns = {
            'entidad': 'Entidad',
            'poblacion': 'Población impactada',
            'fecha_ejecucion': 'Fecha final de ejecución',
            'resumen': 'Resumen de actividades',
            'descripcion': 'Descripción de los compromisos'
        }
    
    def generate_participacion_chart(self, data: List[Dict]) -> Dict:
        """
        Genera el gráfico de participación por entidad
        """
        if not data:
            return {}
        
        # Contar actividades por entidad
        entidad_key = self.important_columns['entidad']
        entity_counts = Counter(row.get(entidad_key, 'Sin entidad') for row in data)
        total_activities = sum(entity_counts.values())
        
        # Calcular porcentajes
        entities = []
        percentages = []
        colors = []
        
        for entity, count in entity_counts.most_common():
            percentage = (count / total_activities) * 100
            entities.append(entity)
            percentages.append(percentage)
            
            # Asignar color basado en la entidad
            if 'Alcaldía' in entity:
                colors.append(self.colors['alcaldia'])  # Rojo para Alcaldía
            else:
                colors.append(self.colors['default'])  # Verde para otras entidades
        
        # Crear gráfico de pie
        fig = go.Figure(data=[go.Pie(
            labels=entities,
            values=percentages,
            hole=0.4,
            textinfo='percent',
            textposition='inside',
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>' +
                         'Porcentaje: %{percent:.1f}%<br>' +
                         'Actividades: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=[entity_counts[entity] for entity in entities]
        )])
        
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=400
        )
        
        return {
            'chart_json': fig.to_json(),
            'top_entities': self._get_top_entities(entity_counts)
        }
    
    def generate_diario_chart(self, data: List[Dict]) -> Dict:
        """
        Genera el gráfico de barras diarias
        """
        if not data:
            return {}
        
        # Filtrar actividades con fechas válidas
        fecha_key = self.important_columns['fecha_ejecucion']
        activities_with_dates = [
            row for row in data 
            if row.get(fecha_key)
        ]
        
        if not activities_with_dates:
            return {}
        
        # Contar actividades por día
        daily_counts = Counter()
        for row in activities_with_dates:
            date_str = row.get(fecha_key)
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    daily_counts[date_obj] += 1
                except ValueError:
                    continue
        
        if not daily_counts:
            return {}
        
        # Ordenar por fecha
        sorted_dates = sorted(daily_counts.keys())
        dates = [date.strftime('%Y-%m-%d') for date in sorted_dates]
        counts = [daily_counts[date] for date in sorted_dates]
        
        # Asignar colores por mes
        colors = []
        for date in sorted_dates:
            month_name = date.strftime('%B').lower()
            if month_name in self.colors:
                colors.append(self.colors[month_name])
            else:
                colors.append(self.colors['default'])  # Color por defecto
        
        # Crear gráfico de barras
        fig = go.Figure(data=[go.Bar(
            x=dates,
            y=counts,
            marker_color=colors,
            hovertemplate='<b>Fecha: %{x}</b><br>' +
                         'Actividades: %{y}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title='Actividades por Día',
            xaxis_title='Fecha',
            yaxis_title='Número de Actividades',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # Crear leyenda personalizada por mes
        legend_data = self._create_month_legend(sorted_dates)
        
        return {
            'chart_json': fig.to_json(),
            'legend_data': legend_data
        }
    
    def _get_top_entities(self, entity_counts: Counter) -> List[Dict]:
        """
        Obtiene el top 3 de entidades con más participación
        """
        sorted_entities = entity_counts.most_common()
        
        # Si hay empate en el primer lugar, asegurar que Alcaldía esté en segundo
        top_entities = []
        alcaldia_found = False
        
        for entity, count in sorted_entities[:3]:
            if 'Alcaldía' in entity and not alcaldia_found:
                # Si Alcaldía no está en el top 3, insertarla en segundo lugar
                if len(top_entities) == 0:
                    top_entities.append({'entity': entity, 'count': count})
                else:
                    top_entities.insert(1, {'entity': entity, 'count': count})
                alcaldia_found = True
            else:
                if len(top_entities) < 3:
                    top_entities.append({'entity': entity, 'count': count})
        
        return top_entities[:3]
    
    def _create_month_legend(self, dates: List[datetime]) -> List[Dict]:
        """
        Crea datos para la leyenda personalizada por mes
        """
        month_colors = {}
        for date in dates:
            month_name = date.strftime('%B').lower()
            if month_name in self.colors:
                month_colors[month_name] = self.colors[month_name]
        
        legend_data = []
        for month, color in month_colors.items():
            legend_data.append({
                'month': month.capitalize(),
                'color': color
            })
        
        return legend_data
    
    def create_monthly_chart(self, entity: str) -> Dict:
        """
        Crea el gráfico mensual para una entidad específica
        """
        entity_data = self.data_manager.get_entity_data(entity)
        activities_with_dates = entity_data.get('activities_with_dates', [])
        
        if not activities_with_dates:
            return {}
        
        # Contar actividades por mes
        monthly_counts = Counter()
        fecha_key = self.important_columns['fecha_ejecucion']
        for row in activities_with_dates:
            date_str = row.get(fecha_key)
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_counts[month_key] += 1
                except ValueError:
                    continue
        
        if not monthly_counts:
            return {}
        
        # Ordenar por mes
        sorted_months = sorted(monthly_counts.keys())
        months = [month for month in sorted_months]
        counts = [monthly_counts[month] for month in sorted_months]
        
        # Crear gráfico de barras
        fig = go.Figure(data=[go.Bar(
            x=months,
            y=counts,
            marker_color=self.colors['default'],
            hovertemplate='<b>Mes: %{x}</b><br>' +
                         'Actividades: %{y}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'Actividades Mensuales - {entity}',
            xaxis_title='Mes',
            yaxis_title='Número de Actividades',
            height=300,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return {
            'chart_json': fig.to_json(),
            'activities_without_dates': entity_data.get('activities_without_dates', [])
        }
    
    def get_entity_summary(self, entity: str) -> Dict:
        """
        Obtiene el resumen de actividades de una entidad
        """
        entity_data = self.data_manager.get_entity_data(entity)
        activities_with_dates = entity_data.get('activities_with_dates', [])
        
        # Crear resumen de actividades
        summary = []
        resumen_key = self.important_columns['resumen']
        fecha_key = self.important_columns['fecha_ejecucion']
        
        for row in activities_with_dates:
            summary.append({
                'activity': row.get(resumen_key, 'Sin descripción'),
                'date': row.get(fecha_key, 'Sin fecha')
            })
        
        return {
            'summary': summary,
            'activities_without_dates': entity_data.get('activities_without_dates', [])
        } 