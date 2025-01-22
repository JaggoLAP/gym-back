from ..database import DatabaseConnection

class Cuota:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.id_socio = kwargs.get('id_socio')
        self.fecha_inicio = kwargs.get('fecha_inicio')
        self.fecha_fin = kwargs.get('fecha_fin')
        self.estado = kwargs.get('estado', 'pendiente')

    def serialize(self):
        return {
            'id': self.id,
            'id_socio': self.id_socio,
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d') if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else None,
            'estado': self.estado
        }

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gym_management.cuotas"
        results = DatabaseConnection.fetch_all(query)
        print("results: ",results)
        return [cls(**row) for row in results]

    @classmethod
    def get_by_id(cls, cuota_id):
        query = "SELECT * FROM gym_management.cuotas WHERE id = %s"
        params = (cuota_id,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return cls(**result) if result else None

    @classmethod
    def create(cls, cuota):
        query = """INSERT INTO gym_management.cuotas (id_socio, fecha_inicio, fecha_fin, estado)
                   VALUES (%s, %s, %s, %s)"""
        params = (cuota.id_socio, cuota.fecha_inicio, cuota.fecha_fin, cuota.estado)
        DatabaseConnection.execute_query(query, params=params)
