from flask import Blueprint
from ..controllers.cuota_controller import CuotaController

cuotas_bp = Blueprint('cuotas_bp', __name__)

cuotas_bp.route('/pagar', methods=['POST'])(CuotaController.pagar_cuota)
cuotas_bp.route('/', methods=['GET'])(CuotaController.get_all)  #  Listar todas las cuotas
cuotas_bp.route('/<int:id_cuota>', methods=['GET'])(CuotaController.get_by_id)  # Obtener una cuota específica
