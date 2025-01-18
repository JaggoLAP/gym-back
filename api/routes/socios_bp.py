from flask import Blueprint
from ..controllers.socio_controller import SocioController

socios_bp = Blueprint('socios_bp', __name__)

socios_bp.route('/', methods=['GET'])(SocioController.get_all)
socios_bp.route('/<int:id_socio>', methods=['GET'])(SocioController.get_by_id)
socios_bp.route('/', methods=['POST'])(SocioController.create)
socios_bp.route('/<int:id_socio>', methods=['PUT'])(SocioController.update)
socios_bp.route('/<int:id_socio>', methods=['DELETE'])(SocioController.delete)
