from ..database import DatabaseConnection

class Cuota:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.socio_id = kwargs.get('socio_id')
        self.fecha_pago = kwargs.get('fecha_pago')
        self.fecha_inicio = kwargs.get('fecha_inicio')
        self.fecha_fin = kwargs.get('fecha_fin')
        self.estado = kwargs.get('estado', 'vencida')
        self.monto = kwargs.get('monto')

    def serialize(self):
        return {
            'id': self.id,
            'socio_id': self.socio_id,
            'fecha_pago': self.fecha_pago.strftime('%Y-%m-%d') if self.fecha_inicio else None,
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d') if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else None,
            'estado': self.estado,
            'monto': self.monto
        }

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gym_management.cuotas"
        results = DatabaseConnection.fetch_all(query)

        cuotas = []

        if results is not None:
            for result in results:
                cuotas.append(cls(
                    id=result[0],
                    socio_id=result[1],
                    fecha_pago=result[2],
                    fecha_inicio=result[3],
                    fecha_fin=result[4],
                    estado=result[5],
                    monto=result[6]
                ))
            return cuotas
        else:
            return None

    @classmethod
    def get_by_id(cls, cuota_id):
        query = "SELECT * FROM gym_management.cuotas WHERE id = %s"
        params = (cuota_id,)
        result = DatabaseConnection.fetch_one(query, params=params)
        
        if result is not None:
            return cls(
                id=result[0],
                socio_id=result[1],
                fecha_pago=result[2],
                fecha_inicio=result[3],
                fecha_fin=result[4],
                estado=result[5],
                monto=result[6]
            )
        else:
            return None

    @classmethod
    def create(cls, cuota):
        query = """INSERT INTO gym_management.cuotas (socio_id, fecha_pago, fecha_inicio, fecha_fin, estado, monto)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (cuota.socio_id, cuota.fecha_pago, cuota.fecha_inicio, cuota.fecha_fin, cuota.estado, cuota.monto)
        DatabaseConnection.execute_query(query, params=params)
        