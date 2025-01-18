from flask import request
from ..models.socio_model import Socio

class SocioController:

    @classmethod
    def get_all(cls):
        socios = Socio.get_all()
        return [socio.serialize() for socio in socios], 200

    @classmethod
    def get_by_id(cls, id_socio):
        socio = Socio.get_by_id(id_socio)
        if not socio:
            return {"message": "Socio no encontrado"}, 404
        return socio.serialize(), 200

    @classmethod
    def create(cls):
        data = request.json
        nuevo_socio = Socio(**data)
        Socio.create(nuevo_socio)
        return {"message": "Socio creado exitosamente"}, 201

    @classmethod
    def update(cls, id_socio):
        data = request.json
        data['id'] = id_socio
        socio_actualizado = Socio(**data)
        updated = Socio.update(socio_actualizado)
        if not updated:
            return {"message": "Socio no encontrado"}, 404
        return {"message": "Socio actualizado exitosamente"}, 200

    @classmethod
    def delete(cls, id_socio):
        deleted = Socio.delete(id_socio)
        if not deleted:
            return {"message": "Socio no encontrado"}, 404
        return {"message": "Socio eliminado exitosamente"}, 204
