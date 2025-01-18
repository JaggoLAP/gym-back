from ..models.user_models import User
from flask import request

class UserController:
    
    @classmethod
    def get(cls):
        users = []
        for user in User.get():
            users.append(user.serialize())
        return users, 200
    
    @classmethod
    def get_by_id(cls, id_usuario):
        user = User(id_usuario=id_usuario)
        result = User.get(user)
        if result is not None:
            return result.serialize(), 200
        else:
            return {'message': 'Usuario no encontrado'}, 404
        
    @classmethod
    def create(cls):
        data = request.json
        print(f'data: {data}')
        user = User(**data)
        print(f'user: {user}')
        user.create(user)
        return {'message': 'user created successfully'}, 201
    
    @classmethod
    def update(cls, id_usuario):
        data = request.json
        data['id_usuario'] = id_usuario
        user = User(**data)
        User.update(user)
        return {'message': 'user updated successfully'}, 200
    
    @classmethod
    def delete(cls, id_usuario):
        user = User(id_usuario=id_usuario)
        User.delete(user)
        return {'message': 'User deleted successfully'}, 204
