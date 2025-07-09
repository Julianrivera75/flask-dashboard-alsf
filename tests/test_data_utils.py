"""
Tests para utilidades de datos
"""

import pytest
from utils.data_utils import (
    clean_numeric_value,
    clean_text_value,
    validate_required_fields,
    aggregate_data_by_field,
    calculate_statistics
)

class TestDataUtils:
    """Tests para funciones de utilidades de datos"""
    
    def test_clean_numeric_value_with_float(self):
        """Test limpieza de valor numérico float"""
        assert clean_numeric_value(123.45) == 123.45
        assert clean_numeric_value(0) == 0.0
    
    def test_clean_numeric_value_with_string(self):
        """Test limpieza de valor numérico string"""
        assert clean_numeric_value("123.45") == 123.45
        assert clean_numeric_value("1,234.56") == 1234.56
        assert clean_numeric_value("abc") == 0.0
        assert clean_numeric_value("") == 0.0
    
    def test_clean_numeric_value_with_none(self):
        """Test limpieza de valor numérico None"""
        assert clean_numeric_value(None) == 0.0
    
    def test_clean_text_value(self):
        """Test limpieza de valor de texto"""
        assert clean_text_value("  hello world  ") == "hello world"
        assert clean_text_value("") == ""
        assert clean_text_value(None) == ""
        assert clean_text_value(123) == "123"
    
    def test_validate_required_fields_valid_data(self):
        """Test validación de campos requeridos con datos válidos"""
        data = [
            {'Entidad': 'Test', 'Actividad': 'Test', 'Fecha': '2025-01-01'},
            {'Entidad': 'Test2', 'Actividad': 'Test2', 'Fecha': '2025-01-02'}
        ]
        required = ['Entidad', 'Actividad', 'Fecha']
        
        result = validate_required_fields(data, required)
        
        assert result['valid'] is True
        assert result['missing_fields'] == []
        assert result['total_records'] == 2
    
    def test_validate_required_fields_missing_fields(self):
        """Test validación de campos requeridos con campos faltantes"""
        data = [
            {'Entidad': 'Test', 'Actividad': 'Test'},  # Falta Fecha
            {'Entidad': 'Test2', 'Fecha': '2025-01-02'}  # Falta Actividad
        ]
        required = ['Entidad', 'Actividad', 'Fecha']
        
        result = validate_required_fields(data, required)
        
        assert result['valid'] is False
        assert 'Fecha' in result['missing_fields']
        assert len(result['invalid_records']) > 0
    
    def test_validate_required_fields_empty_data(self):
        """Test validación de campos requeridos con datos vacíos"""
        data = []
        required = ['Entidad', 'Actividad', 'Fecha']
        
        result = validate_required_fields(data, required)
        
        assert result['valid'] is False
        assert result['missing_fields'] == required
        assert result['total_records'] == 0
    
    def test_aggregate_data_by_field(self):
        """Test agregación de datos por campo"""
        data = [
            {'Entidad': 'A', 'Valor': 10},
            {'Entidad': 'B', 'Valor': 20},
            {'Entidad': 'A', 'Valor': 15},
            {'Entidad': 'C', 'Valor': 30}
        ]
        
        result = aggregate_data_by_field(data, 'Entidad', 'Valor')
        
        assert 'A' in result
        assert 'B' in result
        assert 'C' in result
        assert result['A']['count'] == 2
        assert result['A']['total_value'] == 25.0
        assert result['B']['count'] == 1
        assert result['B']['total_value'] == 20.0
    
    def test_calculate_statistics(self):
        """Test cálculo de estadísticas"""
        data = [
            {'Valor': 10},
            {'Valor': 20},
            {'Valor': 30},
            {'Valor': 40}
        ]
        
        stats = calculate_statistics(data, 'Valor')
        
        assert stats['count'] == 4
        assert stats['sum'] == 100.0
        assert stats['average'] == 25.0
        assert stats['min'] == 10.0
        assert stats['max'] == 40.0
    
    def test_calculate_statistics_empty_data(self):
        """Test cálculo de estadísticas con datos vacíos"""
        data = []
        
        stats = calculate_statistics(data, 'Valor')
        
        assert stats['count'] == 0
        assert stats['sum'] == 0.0
        assert stats['average'] == 0.0
        assert stats['min'] == 0.0
        assert stats['max'] == 0.0 