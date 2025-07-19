import pytest
from unittest.mock import patch, MagicMock
from views.views import existe_evaluacion


class TestUtilityFunctions:
    """Pruebas para funciones utilitarias"""
    
    @patch('views.views.db')
    def test_existe_evaluacion_true(self, mock_db):
        """Debe retornar True cuando existe una evaluación con el nombre dado"""

        mock_evaluacion = MagicMock()
        mock_db.session.query.return_value.filter.return_value.first.return_value = mock_evaluacion

        resultado = existe_evaluacion("Evaluación Existente")

        assert resultado is True

    @patch('views.views.db')
    def test_existe_evaluacion_false(self, mock_db):
        """Debe retornar False cuando no existe una evaluación con el nombre dado"""

        mock_db.session.query.return_value.filter.return_value.first.return_value = None

        resultado = existe_evaluacion("Evaluación Inexistente")

        assert resultado is False

    @patch('views.views.db')
    def test_existe_evaluacion_nombre_vacio(self, mock_db):
        """Debe manejar correctamente nombres vacíos"""

        mock_db.session.query.return_value.filter.return_value.first.return_value = None

        resultado = existe_evaluacion("")

        assert resultado is False

    @patch('views.views.db')
    def test_existe_evaluacion_nombre_none(self, mock_db):
        """Debe manejar correctamente cuando el nombre es None"""
        mock_db.session.query.return_value.filter.return_value.first.return_value = None

        resultado = existe_evaluacion(None)

        assert resultado is False 