from flask import request
from ..models.actividad_model import Actividad

class ActividadController:

    @classmethod
    def get_all(cls):
        actividades = Actividad.get_all_disponibles()
        return [actividad.serialize() for actividad in actividades], 200

    @classmethod
    def create(cls):
        data = request.json
        nueva_actividad = Actividad(**data)
        Actividad.create(nueva_actividad)
        return {"message": "Actividad creada exitosamente"}, 201

    @classmethod
    def get_by_id(cls, id_actividad):
        actividad = Actividad.get_by_id(id_actividad)
        if not actividad:
            return {"message": "Actividad no encontrada"}, 404
        return actividad.serialize(), 200

    @classmethod
    def update(cls, id_actividad):
        data = request.json
        data['id'] = id_actividad
        actividad_actualizada = Actividad(**data)
        updated = Actividad.update(actividad_actualizada)
        if not updated:
            return {"message": "Actividad no encontrada"}, 404
        return {"message": "Actividad actualizada exitosamente"}, 200

    @classmethod
    def delete(cls, id_actividad):
        deleted = Actividad.delete(id_actividad)
        if not deleted:
            return {"message": "Actividad no encontrada"}, 404
        return {"message": "Actividad eliminada exitosamente"}, 204
