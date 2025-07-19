import pytest
import os
import sys
from unittest.mock import MagicMock, patch

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

@pytest.fixture
def app():
    """Fixture para la aplicación Flask configurada para testing"""
    os.environ['TESTING'] = 'True'
    
    # Mock de la base de datos antes de importar la app
    with patch('models.models.db') as mock_db, \
         patch('views.views.db', mock_db), \
         patch('app.db', mock_db):
        
        # Configurar el mock de la base de datos
        mock_session = MagicMock()
        mock_db.session = mock_session
        mock_db.init_app = MagicMock()
        mock_db.create_all = MagicMock()
        
        # Mock de SQLAlchemy methods
        mock_db.Model = MagicMock()
        mock_db.Column = MagicMock()
        mock_db.String = MagicMock()
        mock_db.Integer = MagicMock()
        mock_db.DateTime = MagicMock()
        mock_db.Boolean = MagicMock()
        
        from app import app as flask_app
        flask_app.config['TESTING'] = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        with flask_app.app_context():
            yield flask_app
    
    # Limpiar variable de entorno
    if 'TESTING' in os.environ:
        del os.environ['TESTING']



@pytest.fixture
def client(app):
    """Fixture para el cliente de testing de Flask"""
    return app.test_client()

@pytest.fixture
def mock_evaluacion():
    """Fixture que devuelve un objeto evaluación mock"""
    evaluacion = MagicMock()
    evaluacion.id = "test-uuid-123"
    evaluacion.id_consecutivo = 1
    evaluacion.nombre = "Evaluación Test"
    evaluacion.esta_eliminada = False
    return evaluacion 