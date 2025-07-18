import uuid

from flask import request
from flask_restful import Resource
from sqlalchemy import func

from models import db, Evaluaciones, EvaluacionesSchema

evaluacion_schema = EvaluacionesSchema()
evaluaciones_schema = EvaluacionesSchema(many=True)


def existe_evaluacion(nombre):
    """
    Verifica si ya existe una evaluacion con el mismo nombre.
    """
    return db.session.query(Evaluaciones).filter((Evaluaciones.nombre == nombre)).first() is not None


class EvaluacionesView(Resource):

    def post(self):
        data = request.get_json()
        required_fields = ["nombre"]
        for field in required_fields:
            if field not in data:
                return {'message': 'El campo nombre es obligatorio'}, 400
        nombre = data["nombre"]
        if existe_evaluacion(nombre):
            return {'message': 'la evaluacion con ese nombre ya existe'}, 412
        try:
            max_consecutivo = db.session.query(func.max(Evaluaciones.id_consecutivo)).scalar()
            nuevo_consecutivo = (max_consecutivo or 0) + 1
            nueva_evaluacion = Evaluaciones(
                id=str(uuid.uuid4()),
                id_consecutivo=nuevo_consecutivo,
                nombre=nombre
            )
            db.session.add(nueva_evaluacion)
            db.session.commit()
            return {
                "id": nueva_evaluacion.id,
                "id_consecutivo": nueva_evaluacion.id_consecutivo,
                "nombre": nueva_evaluacion.nombre,
                "message": "Evaluacion creada correctamente"
            }, 201
        except Exception as e:
            return {'message': f'Hubo un problema al crear la cuenta: {str(e)}'}, 500

    def get(self):
        try:
            evaluaciones = db.session.query(Evaluaciones).filter_by(esta_eliminada=False).all()
            resultado = evaluaciones_schema.dump(evaluaciones)
            return resultado, 200
        except Exception as e:
            return {'message': f'Hubo un error al obtener las evaluaciones: {str(e)}'}, 500


class EvaluacionDetailView(Resource):

    def put(self, id):
        if not id:
            return {'message': 'El ID de la evaluación es obligatorio'}, 400
        data = request.get_json()
        if not data or 'nombre' not in data:
            return {'message': 'El campo "nombre" es obligatorio'}, 400
        evaluacion = db.session.query(Evaluaciones).filter_by(id=id, esta_eliminada=False).first()
        if not evaluacion:
            return {'message': 'Evaluación no encontrada'}, 404
        evaluacion.nombre = data['nombre']
        try:
            db.session.commit()
            return {
                "id": id,
                "id_consecutivo": evaluacion.id_consecutivo,
                "nombre": evaluacion.nombre,
                "message": "Evaluacion actualizada correctamente"
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error al actualizar la evaluación: {str(e)}'}, 500

    def delete(self, id):
        if not id:
            return {'message': 'El ID de la evaluación es obligatorio'}, 400
        evaluacion = db.session.query(Evaluaciones).filter_by(id=id, esta_eliminada=False).first()
        if not evaluacion:
            return {'message': 'Evaluación no encontrada'}, 404
        evaluacion.esta_eliminada = True
        try:
            db.session.commit()
            return {'message': 'Evaluación eliminada correctamente'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error al eliminar la evaluación: {str(e)}'}, 500


class HealthCheckView(Resource):
    def get(self):
        """
        Usado para verificar el estado del servicio.
        """
        return "pong", 200


class ResetDatabaseView(Resource):
    def post(self):
        """
        Usado para limpiar la base de datos del servicio.
        """
        try:
            db.session.query(Evaluaciones).delete()
            db.session.commit()
            return {"message": "Todos los datos fueron eliminados"}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': f'Hubo un problema al eliminar la base de datos: {str(e)}'}, 500
