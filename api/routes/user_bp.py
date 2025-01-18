from flask import Blueprint
from ..controllers.user_controller import UserController

users_bp = Blueprint('user_bp', __name__)

users_bp.route('/', methods=['GET'])(UserController.get)
users_bp.route('/<int:id_usuario>', methods=['GET'])(UserController.get_by_id)
users_bp.route('/', methods=['POST'])(UserController.create)
users_bp.route('/<int:id_usuario>', methods=['PUT'])(UserController.update)
users_bp.route('/<int:id_usuario>', methods=['DELETE'])(UserController.delete)