import json
import pytest
from unittest.mock import patch, MagicMock


class TestEvaluacionDetailViewPut:
    """Pruebas para el endpoint PUT /evaluaciones/<id>"""
    
    @patch('views.views.db')
    def test_actualizar_evaluacion_id_vacio_directo(self, mock_db, app):
        """Debe retornar error 400 cuando el ID está vacío (test directo del método)"""

        from views.views import EvaluacionDetailView
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        view = EvaluacionDetailView()

        with app.test_request_context(json={"nombre": "Nuevo Nombre"}):

            result = view.put("")

            assert result[1] == 400
            assert result[0]['message'] == 'El ID de la evaluación es obligatorio'

    @patch('views.views.db')
    def test_actualizar_evaluacion_exitosa(self, mock_db, client):
        """Debe actualizar una evaluación exitosamente"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-123"
        mock_evaluacion = MagicMock()
        mock_evaluacion.id = evaluacion_id
        mock_evaluacion.id_consecutivo = 1
        mock_evaluacion.nombre = "Nombre Original"
        mock_evaluacion.esta_eliminada = False
        
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_evaluacion
        
        data = {"nombre": "Nombre Actualizado"}
        

        response = client.put(f'/evaluaciones/{evaluacion_id}', 
                             data=json.dumps(data),
                             content_type='application/json')
        

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['id'] == evaluacion_id
        assert response_data['id_consecutivo'] == 1
        assert response_data['nombre'] == "Nombre Actualizado"
        assert response_data['message'] == "Evaluacion actualizada correctamente"

        assert mock_evaluacion.nombre == "Nombre Actualizado"
        mock_db.session.commit.assert_called_once()

    def test_actualizar_evaluacion_sin_id(self, client):
        """Debe retornar error 400 cuando no se proporciona ID"""

        data = {"nombre": "Nuevo Nombre"}

        response = client.put('/evaluaciones/', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 404

    def test_actualizar_evaluacion_sin_nombre(self, client):
        """Debe retornar error 400 cuando no se proporciona nombre"""

        evaluacion_id = "test-uuid-123"
        data = {}

        response = client.put(f'/evaluaciones/{evaluacion_id}', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['message'] == 'El campo "nombre" es obligatorio'

    def test_actualizar_evaluacion_nombre_vacio(self, client):
        """Debe permitir actualizar con nombre vacío (comportamiento actual de la aplicación)"""

        evaluacion_id = "test-uuid-123"
        data = {"nombre": ""}
        
        with patch('views.views.db') as mock_db:
            mock_session = MagicMock()
            mock_db.session = mock_session

            mock_evaluacion = MagicMock()
            mock_evaluacion.id = evaluacion_id
            mock_evaluacion.id_consecutivo = 1
            mock_evaluacion.nombre = "Nombre Original"
            mock_evaluacion.esta_eliminada = False
            mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_evaluacion

            response = client.put(f'/evaluaciones/{evaluacion_id}', 
                                 data=json.dumps(data),
                                 content_type='application/json')

            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert response_data['id'] == evaluacion_id
            assert response_data['message'] == "Evaluacion actualizada correctamente"

    @patch('views.views.db')
    def test_actualizar_evaluacion_no_encontrada(self, mock_db, client):
        """Debe retornar error 404 cuando la evaluación no existe"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "uuid-inexistente"
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = None
        
        data = {"nombre": "Nuevo Nombre"}

        response = client.put(f'/evaluaciones/{evaluacion_id}', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Evaluación no encontrada'

    @patch('views.views.db')
    def test_actualizar_evaluacion_eliminada(self, mock_db, client):
        """Debe retornar error 404 cuando la evaluación está eliminada"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-eliminada"
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = None
        
        data = {"nombre": "Nuevo Nombre"}

        response = client.put(f'/evaluaciones/{evaluacion_id}', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 404

    @patch('views.views.db')
    def test_actualizar_evaluacion_error_base_datos(self, mock_db, client):
        """Debe retornar error 500 cuando hay problema con la base de datos"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-123"
        mock_evaluacion = MagicMock()
        mock_evaluacion.id = evaluacion_id
        mock_evaluacion.id_consecutivo = 1
        mock_evaluacion.esta_eliminada = False
        
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_evaluacion
        mock_db.session.commit.side_effect = Exception("Error de BD")
        
        data = {"nombre": "Nuevo Nombre"}
        

        response = client.put(f'/evaluaciones/{evaluacion_id}', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "Error al actualizar la evaluación" in response_data['message']
        mock_db.session.rollback.assert_called_once()


class TestEvaluacionDetailViewDelete:
    """Pruebas para el endpoint DELETE /evaluaciones/<id>"""
    
    @patch('views.views.db')
    def test_eliminar_evaluacion_id_vacio_directo(self, mock_db):
        """Debe retornar error 400 cuando el ID está vacío (test directo del método)"""

        from views.views import EvaluacionDetailView
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        view = EvaluacionDetailView()

        result = view.delete("")

        assert result[1] == 400
        assert result[0]['message'] == 'El ID de la evaluación es obligatorio'

    @patch('views.views.db')
    def test_eliminar_evaluacion_exitosa(self, mock_db, client):
        """Debe eliminar una evaluación exitosamente (soft delete)"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-123"
        mock_evaluacion = MagicMock()
        mock_evaluacion.id = evaluacion_id
        mock_evaluacion.esta_eliminada = False
        
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_evaluacion

        response = client.delete(f'/evaluaciones/{evaluacion_id}')

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Evaluación eliminada correctamente'

        assert mock_evaluacion.esta_eliminada == True
        mock_db.session.commit.assert_called_once()

    def test_eliminar_evaluacion_sin_id(self, client):
        """Debe retornar error 404 cuando no se proporciona ID"""

        response = client.delete('/evaluaciones/')

        assert response.status_code == 404

    @patch('views.views.db')
    def test_eliminar_evaluacion_no_encontrada(self, mock_db, client):
        """Debe retornar error 404 cuando la evaluación no existe"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "uuid-inexistente"
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = None

        response = client.delete(f'/evaluaciones/{evaluacion_id}')
        

        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Evaluación no encontrada'

    @patch('views.views.db')
    def test_eliminar_evaluacion_ya_eliminada(self, mock_db, client):
        """Debe retornar error 404 cuando la evaluación ya está eliminada"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-eliminada"
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = None

        response = client.delete(f'/evaluaciones/{evaluacion_id}')

        assert response.status_code == 404

    @patch('views.views.db')
    def test_eliminar_evaluacion_error_base_datos(self, mock_db, client):
        """Debe retornar error 500 cuando hay problema con la base de datos"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        evaluacion_id = "test-uuid-123"
        mock_evaluacion = MagicMock()
        mock_evaluacion.id = evaluacion_id
        mock_evaluacion.esta_eliminada = False
        
        mock_db.session.query.return_value.filter_by.return_value.first.return_value = mock_evaluacion
        mock_db.session.commit.side_effect = Exception("Error de BD")

        response = client.delete(f'/evaluaciones/{evaluacion_id}')
        
        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "Error al eliminar la evaluación" in response_data['message']
        mock_db.session.rollback.assert_called_once() 