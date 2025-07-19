import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Evaluaciones(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    id_consecutivo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(140))
    instrucciones = db.Column(db.Text, nullable=True)
    nombre_formulario = db.Column(db.String(200), nullable=True)
    fecha_insercion = db.Column(db.DateTime, default=lambda: datetime.datetime.now(pytz.utc), nullable=False)
    esta_eliminada = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, id, id_consecutivo, nombre, instrucciones=None, nombre_formulario=None, fecha_insercion=None, esta_eliminada=False):
        self.id = id
        self.id_consecutivo = id_consecutivo
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.nombre_formulario = nombre_formulario
        self.fecha_insercion = fecha_insercion or datetime.datetime.now(pytz.utc)
        self.esta_eliminada = esta_eliminada

    def __repr__(self):
        return f"{self.id} - {self.id_consecutivo} - {self.nombre} - {self.instrucciones} - {self.nombre_formulario} - {self.fecha_insercion} - {self.esta_eliminada}"


class EvaluacionesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Evaluaciones
        include_relationships = False
        load_instance = True
