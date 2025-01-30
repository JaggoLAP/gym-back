from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.controllers.auth_controller import authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Maneja la autenticación del usuario."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"message": "Credenciales inválidas"}), 401

    token = create_access_token(identity={"id": user["id"]})
    return jsonify({"access_token": token}), 200
