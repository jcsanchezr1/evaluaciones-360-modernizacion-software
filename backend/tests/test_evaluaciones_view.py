import json
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import func


class TestEvaluacionesViewPost:
    """Pruebas para el endpoint POST /evaluaciones"""
    
    @patch('views.views.existe_evaluacion')
    @patch('views.views.uuid.uuid4')
    @patch('views.views.db')
    def test_crear_evaluacion_exitosa(self, mock_db, mock_uuid, mock_existe_evaluacion, client):
        """Debe crear una evaluación nueva exitosamente"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_uuid.return_value = "test-uuid-123"
        mock_existe_evaluacion.return_value = False
        mock_db.session.query.return_value.scalar.return_value = 5
        
        data = {"nombre": "Nueva Evaluación"}

        response = client.post('/evaluaciones', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['id'] == "test-uuid-123"
        assert response_data['id_consecutivo'] == 6
        assert response_data['nombre'] == "Nueva Evaluación"
        assert response_data['message'] == "Evaluacion creada correctamente"

        mock_existe_evaluacion.assert_called_once_with("Nueva Evaluación")
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()
    
    @patch('views.views.existe_evaluacion')
    @patch('views.views.uuid.uuid4')
    @patch('views.views.db')
    def test_crear_evaluacion_primer_consecutivo(self, mock_db, mock_uuid, mock_existe_evaluacion, client):
        """Debe crear evaluación con consecutivo 1 cuando no hay evaluaciones previas"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_uuid.return_value = "test-uuid-456"
        mock_existe_evaluacion.return_value = False
        mock_db.session.query.return_value.scalar.return_value = None
        
        data = {"nombre": "Primera Evaluación"}

        response = client.post('/evaluaciones', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['id_consecutivo'] == 1

    def test_crear_evaluacion_sin_nombre(self, client):
        """Debe retornar error 400 cuando no se proporciona el nombre"""

        data = {}

        response = client.post('/evaluaciones', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['message'] == 'El campo nombre es obligatorio'

    def test_crear_evaluacion_nombre_vacio(self, client):
        """Debe retornar error 412 cuando el nombre está vacío pero existe_evaluacion se ejecuta"""
        data = {"nombre": ""}
        
        with patch('views.views.existe_evaluacion') as mock_existe_evaluacion, \
             patch('views.views.db') as mock_db:
            
            mock_existe_evaluacion.return_value = True
            mock_session = MagicMock()
            mock_db.session = mock_session

            response = client.post('/evaluaciones', 
                                 data=json.dumps(data),
                                 content_type='application/json')

            assert response.status_code == 412

    @patch('views.views.existe_evaluacion')
    def test_crear_evaluacion_nombre_duplicado(self, mock_existe_evaluacion, client):
        """Debe retornar error 412 cuando ya existe una evaluación con el mismo nombre"""

        mock_existe_evaluacion.return_value = True
        data = {"nombre": "Evaluación Existente"}
        

        response = client.post('/evaluaciones', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 412
        response_data = json.loads(response.data)
        assert response_data['message'] == 'la evaluacion con ese nombre ya existe'

    @patch('views.views.existe_evaluacion')
    @patch('views.views.uuid.uuid4')
    @patch('views.views.db')
    def test_crear_evaluacion_error_base_datos(self, mock_db, mock_uuid, mock_existe_evaluacion, client):
        """Debe retornar error 500 cuando hay un problema con la base de datos"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_uuid.return_value = "test-uuid-789"
        mock_existe_evaluacion.return_value = False
        mock_db.session.query.return_value.scalar.return_value = 1
        mock_db.session.commit.side_effect = Exception("Error de BD")
        
        data = {"nombre": "Evaluación Test"}

        response = client.post('/evaluaciones', 
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "Hubo un problema al crear la cuenta" in response_data['message']


class TestEvaluacionesViewGet:
    """Pruebas para el endpoint GET /evaluaciones"""
    
    @patch('views.views.evaluaciones_schema')
    @patch('views.views.db')
    def test_obtener_evaluaciones_exitoso(self, mock_db, mock_schema, client):
        """Debe retornar lista de evaluaciones exitosamente"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        
        mock_evaluacion1 = MagicMock()
        mock_evaluacion1.id = "uuid-1"
        mock_evaluacion1.nombre = "Evaluación 1"
        mock_evaluacion1.esta_eliminada = False
        
        mock_evaluacion2 = MagicMock()
        mock_evaluacion2.id = "uuid-2"
        mock_evaluacion2.nombre = "Evaluación 2"
        mock_evaluacion2.esta_eliminada = False
        
        evaluaciones_mock = [mock_evaluacion1, mock_evaluacion2]
        mock_db.session.query.return_value.filter_by.return_value.all.return_value = evaluaciones_mock
        
        expected_result = [
            {"id": "uuid-1", "nombre": "Evaluación 1"},
            {"id": "uuid-2", "nombre": "Evaluación 2"}
        ]
        mock_schema.dump.return_value = expected_result

        response = client.get('/evaluaciones')

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data == expected_result

        mock_db.session.query.return_value.filter_by.assert_called_once_with(esta_eliminada=False)

    @patch('views.views.db')
    def test_obtener_evaluaciones_lista_vacia(self, mock_db, client):
        """Debe retornar lista vacía cuando no hay evaluaciones"""

        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.session.query.return_value.filter_by.return_value.all.return_value = []
        
        with patch('views.views.evaluaciones_schema.dump', return_value=[]):
            response = client.get('/evaluaciones')

            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert response_data == []

    @patch('views.views.db')
    def test_obtener_evaluaciones_error_base_datos(self, mock_db, client):
        """Debe retornar error 500 cuando hay problema con la base de datos"""
        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.session.query.side_effect = Exception("Error de consulta")

        response = client.get('/evaluaciones')

        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "Hubo un error al obtener las evaluaciones" in response_data['message'] 