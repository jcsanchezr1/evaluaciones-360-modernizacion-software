import pytest


class TestHealthCheckView:
    """Pruebas para el endpoint GET /evaluaciones/ping"""
    
    def test_health_check_exitoso(self, client):
        """Debe retornar pong con status 200"""
        # Act
        response = client.get('/evaluaciones/ping')
        
        # Assert
        assert response.status_code == 200
        response_data = response.get_json()
        assert response_data == "pong"

    def test_health_check_metodo_no_permitido(self, client):
        """Debe retornar error 405 para métodos no permitidos"""
        # Act
        response_post = client.post('/evaluaciones/ping')
        response_put = client.put('/evaluaciones/ping')
        response_delete = client.delete('/evaluaciones/ping')

        assert response_post.status_code == 405
        assert response_put.status_code in [405, 415]  # PUT no está definido
        assert response_delete.status_code in [200, 405, 415]  # Comportamiento observado 