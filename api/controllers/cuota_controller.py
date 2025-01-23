from flask import request
from ..models.cuota_model import Cuota
from ..models.socio_model import Socio

class CuotaController:

    @classmethod
    def pagar_cuota(cls):
        data = request.json
        socio_id = data.get('socio_id')
        socio = Socio.get_by_id(socio_id)
        if not socio:
            return {"message": "Socio no encontrado"}, 404

        nueva_cuota = Cuota(
            socio_id=socio_id,
            fecha_pago=data.get('fecha_pago'),
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            estado='activa',
            monto=data['monto']
        )

        Cuota.create(nueva_cuota)

        socio.estado = 'activo'
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
