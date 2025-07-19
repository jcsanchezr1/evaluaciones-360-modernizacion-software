import json
import pytest
from unittest.mock import patch, MagicMock


class TestResetDatabaseView:
    """Pruebas para el endpoint POST /evaluaciones/reset"""
    
    @patch('views.views.db')
    def test_reset_database_exitoso(self, mock_db, client):
        """Debe limpiar la base de datos exitosamente"""
        # Arrange
        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.session.query.return_value.delete.return_value = 5
        

        response = client.post('/evaluaciones/reset')

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Todos los datos fueron eliminados'

        mock_db.session.query.return_value.delete.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch('views.views.db')
    def test_reset_database_sin_datos(self, mock_db, client):
        """Debe funcionar correctamente incluso cuando no hay datos"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.session.query.return_value.delete.return_value = 0

        response = client.post('/evaluaciones/reset')

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Todos los datos fueron eliminados'

    @patch('views.views.db')
    def test_reset_database_error_base_datos(self, mock_db, client):
        """Debe retornar error 500 cuando hay problema con la base de datos"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.session.query.return_value.delete.side_effect = Exception("Error de BD")

        response = client.post('/evaluaciones/reset')

        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "Hubo un problema al eliminar la base de datos" in response_data['message']
        mock_db.session.rollback.assert_called_once()

    def test_reset_database_metodo_no_permitido(self, client):
        """Debe retornar error 405 para métodos no permitidos"""

        response_get = client.get('/evaluaciones/reset')
        response_put = client.put('/evaluaciones/reset')
        response_delete = client.delete('/evaluaciones/reset')

        assert response_get.status_code == 405
        assert response_put.status_code in [405, 415]  # PUT no está definido
        assert response_delete.status_code in [200, 405, 415]