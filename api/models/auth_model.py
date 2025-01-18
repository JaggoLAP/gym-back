from ..database import DatabaseConnection

class User:

    def __init__(self, **kwargs):
        self.id_usuario = kwargs.get('id_usuario')
        self.nombre_usuario = kwargs.get('nombre_usuario')
        self.email = kwargs.get('email')        
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.fecha_nac = kwargs.get('fecha_nac')
        self.contrasena = kwargs.get('contrasena')
        self.imagen_perfil = kwargs.get('imagen_perfil')
        self.estado = kwargs.get('estado')
    
    def serialize(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nac": self.fecha_nac,
            "contrasena": self.contrasena,
            "imagen_perfil": self.imagen_perfil,
            "estado": self.estado
        }

    @classmethod
    def is_registered(cls, user):
        query = """SELECT id_usuario FROM devpro.usuarios \
          WHERE nombre_usuario = %s and contrasena = %s;"""
        params = user.nombre_usuario, user.contrasena
        result = DatabaseConnection.fetch_one(query, params=params)
        
        if result is not None:
            return result
        return None
    
    @classmethod
    def get_auth(cls, user):
        query = """SELECT * FROM devpro.usuarios WHERE nombre_usuario = %s"""
        params = user.nombre_usuario,
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(
                id_usuario = result[0],
                nombre_usuario = result[1],
                email = result[2],
                nombre = result[3],
                apellido = result[4],
                fecha_nac = result[5],
                contrasena = result[6],
                imagen_perfil = result[7],
                estado = result[8]
            )
        return None