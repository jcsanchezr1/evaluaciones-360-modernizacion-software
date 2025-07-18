import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Evaluaciones(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(140))
    fecha_insercion = db.Column(db.DateTime, default=lambda: datetime.datetime.now(pytz.utc), nullable=False)
    esta_eliminada = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, id, nombre, fecha_insercion=None, esta_eliminada=False):
        self.id = id
        self.nombre = nombre
        self.fecha_insercion = fecha_insercion or datetime.datetime.now(pytz.utc)
        self.esta_eliminada = esta_eliminada

    def __repr__(self):
        return f"{self.id} - {self.nombre} - {self.fecha_insercion} - {self.esta_eliminada}"


class EvaluacionesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Evaluaciones
        include_relationships = False
        load_instance = True
