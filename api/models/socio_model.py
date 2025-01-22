from ..database import DatabaseConnection

class Socio:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.email = kwargs.get('email')
        self.telefono = kwargs.get('telefono')
        self.direccion = kwargs.get('direccion')
        self.password = kwargs.get('password')
        self.estado = kwargs.get('estado', 'vencida')
        self.fecha_registro = kwargs.get('fecha_registro')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'password': self.password,
            'estado': self.estado,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d') if self.fecha_registro else None
        }


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gym_management.socios"
        results = DatabaseConnection.fetch_all(query)
        socios = []

        if results is not None:
            for result in results:
                socios.append(cls(
                    id=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    email=result[3],
                    telefono=result[4],
                    direccion=result[5]
                ))
            return socios
        else:
            return None

    @classmethod
    def get_by_id(cls, socio_id):
        query = "SELECT * FROM gym_management.socios WHERE id = %s"
        params = (socio_id,)
        result = DatabaseConnection.fetch_one(query, params=params)
        
        if result is not None:
            return cls(
                id=result[0],
                nombre=result[1],
                apellido=result[2],
                email=result[3],
                telefono=result[4],
                direccion=result[5]
            )
        else:
            return None

    @classmethod
    def create(cls, socio):
        query = """INSERT INTO gym_management.socios (nombre, apellido, email, telefono, direccion, password)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (socio.nombre, socio.apellido, socio.email, socio.telefono, socio.direccion, socio.password)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update(cls, socio):
        query = """UPDATE gym_management.socios
                   SET telefono = %s, direccion = %s, password = %s
                   WHERE id = %s"""
        params = (socio.telefono, socio.direccion, socio.password, socio.id)
        DatabaseConnection.execute_query(query, params=params)
        return True

    @classmethod
    def delete(cls, socio_id):
        query = """SELECT * FROM gym_management.socios WHERE id = %s"""
        params = (socio_id,)
        socioDel = DatabaseConnection.fetch_one(query, params=params)

        if not socioDel:
            print("socioDel no existe ")
            return False

        query_delete = """DELETE FROM gym_management.socios WHERE id = %s"""
        params_delete = (socio_id,)
        DatabaseConnection.execute_query(query_delete, params=params_delete)

        return True
