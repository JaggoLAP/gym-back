from ..database import DatabaseConnection

class Socio:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.email = kwargs.get('email')
        self.estado_membresia = kwargs.get('estado_membresia', 'inactivo')
        self.fecha_registro = kwargs.get('fecha_registro')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'estado_membresia': self.estado_membresia,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d') if self.fecha_registro else None
        }

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM socios"
        results = DatabaseConnection.fetch_all(query)
        return [cls(**row) for row in results]

    @classmethod
    def get_by_id(cls, socio_id):
        query = "SELECT * FROM socios WHERE id = %s"
        params = (socio_id,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return cls(**result) if result else None

    @classmethod
    def create(cls, socio):
        query = """INSERT INTO socios (nombre, apellido, email, estado_membresia, fecha_registro)
                   VALUES (%s, %s, %s, %s, NOW())"""
        params = (socio.nombre, socio.apellido, socio.email, socio.estado_membresia)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update(cls, socio):
        query = """UPDATE socios
                   SET nombre = %s, apellido = %s, email = %s, estado_membresia = %s
                   WHERE id = %s"""
        params = (socio.nombre, socio.apellido, socio.email, socio.estado_membresia, socio.id)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, socio_id):
        query = "DELETE FROM socios WHERE id = %s"
        params = (socio_id,)
        DatabaseConnection.execute_query(query, params=params)
