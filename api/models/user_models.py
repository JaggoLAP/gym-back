from ..database import DatabaseConnection

class User:
    _keys= ['id_usuario', 'nombre_usuario', 'email', 'nombre', 'apellido', 'fecha_nac', 'contrasena', 'imagen_perfil',  'estado']
    def __init__(self, **kwargs) -> None:
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
            'id_usuario':  self.id_usuario,
            'nombre_usuario': self.nombre_usuario,
            'email' : self.email,
            'nombre' : self.nombre,
            'apellido' : self.apellido,
            'fecha_nac': self.fecha_nac,
            'contrasena' : self.contrasena,
            'imagen_perfil': self.imagen_perfil,
            'estado': self.estado
        }
    
    @classmethod
    def create (cls, user):
        query = """INSERT INTO devpro.usuarios (nombre_usuario, email, nombre, apellido, fecha_nac, contrasena) VALUES (%(nombre_usuario)s, %(email)s, %(nombre)s, %(apellido)s, %(fecha_nac)s, %(contrasena)s) """
        params = user.__dict__
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete (cls, user):
        query = """DELETE FROM devpro.usuarios WHERE id_usuario = %s"""
        params = user.id_usuario,
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def get(cls, user=None):
        if user is not None:
            query = """SELECT * FROM devpro.usuarios WHERE id_usuario = %s"""
            params = user.id_usuario,
            result = DatabaseConnection.fetch_one(query, params=params)            
            if result is not None:
                return cls(**dict(zip(cls._keys, result)))
            else:
                return None
        else:
            query = """SELECT * FROM devpro.usuarios"""
            results = DatabaseConnection.fetch_all(query)
            users = []
            for row in results:
                users.append(cls(**dict(zip(cls._keys, row))))
            return users
        
    @classmethod
    def update(cls, user):
        query = """UPDATE devpro.usuarios SET """
        user_data= user.__dict__
        user_updates = []
        for key in user_data.keys():
            if user_data[key] is not None and key != 'id_usuario':
                user_updates.append(f'{key} = %({key})s')
        query+=', '.join(user_updates)
        query+=' WHERE id_usuario = %(id_usuario)s'
        DatabaseConnection.execute_query(query, params=user_data)

    @classmethod
    def is_registered(cls, user):
        query = """SELECT id_usuario FROM devpro.usuarios \
          WHERE nombre_usuario = %s and contrasena = %s;"""
        params = user.nombre_usuario, user.contrasena
        result = DatabaseConnection.fetch_one(query, params=params)
        if result is not None:
            return True
        return False
    
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