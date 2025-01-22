from flask import request
from ..models.cuota_model import Cuota
from ..models.socio_model import Socio

class CuotaController:

    @classmethod
    def pagar_cuota(cls):
        data = request.json
        id_socio = data.get('id_socio')

        socio = Socio.get_by_id(id_socio)
        if not socio:
            return {"message": "Socio no encontrado"}, 404

        nueva_cuota = Cuota(
            id_socio=id_socio,
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            estado='pagada'
        )
        Cuota.create(nueva_cuota)

        # Actualiza el estado del socio
        socio.estado_membresia = 'activo'
        Socio.update(socio)

        return {"message": "Pago registrado y membresía activada"}, 201

    @classmethod
    def get_all(cls):
        cuotas = Cuota.get_all()
        return [cuota.serialize() for cuota in cuotas], 200

    @classmethod
    def get_by_id(cls, id_cuota):
        cuota = Cuota.get_by_id(id_cuota)
        if not cuota:
            return {"message": "Cuota no encontrada"}, 404
        return cuota.serialize(), 200
