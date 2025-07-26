import os
import sys

# Asegurarte de que el directorio actual esté en sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from models import db
from views import EvaluacionesView, EvaluacionDetailView, HealthCheckView, ResetDatabaseView

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

if not os.getenv('TESTING'):
    with app.app_context():
        db.create_all()

cors = CORS(app)
api = Api(app)
api.add_resource(EvaluacionesView, '/evaluaciones')
api.add_resource(EvaluacionDetailView, '/evaluaciones/<string:id>')
api.add_resource(HealthCheckView, '/evaluaciones/ping')
api.add_resource(ResetDatabaseView, '/evaluaciones/reset')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
