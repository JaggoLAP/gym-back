from ..models.auth_model import User

from flask import request, session

class AuthController:

    @classmethod
    def login(cls):
        data = request.json
        user = User(
            id_usuario = data.get('id_usuario'),
            nombre_usuario = data.get('nombre_usuario'),
            contrasena = data.get('contrasena')
        )
        
        result = User.is_registered(user)
        if result is not None:
            session['nombre_usuario'] = data.get('nombre_usuario')
            session['id_usuario'] = result[0]
            return {"message": "Sesion iniciada"}, 200
        else:
            return {"message": "Usuario o contraseña incorrectos"}, 401

    @classmethod
    def show_profile(cls):
        nombre_usuario = session.get('nombre_usuario')
        print(f'nombre_usuario session: {session.get("nombre_usuario")}')
        if nombre_usuario is None:
            return {"message": "Usuario no encontrado"}, 404
        else:
            user = User.get_auth(User(nombre_usuario = nombre_usuario))
            if user is None:
                return {"message": "Usuario no encontrado"}, 404
            else:
                return user.serialize(), 200
    
    @classmethod
    def logout(cls):
        session.pop('nombre_usuario', None)
        session.clear()
        return {"message": "Sesion cerrada"}, 200