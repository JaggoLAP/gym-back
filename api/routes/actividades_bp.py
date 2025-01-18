from flask import Blueprint
from ..controllers.actividad_controller import ActividadController

actividades_bp = Blueprint('actividades_bp', __name__)

actividades_bp.route('/', methods=['GET'])(ActividadController.get_all)
actividades_bp.route('/', methods=['POST'])(ActividadController.create)  # Crear nueva actividad
actividades_bp.route('/<int:id_actividad>', methods=['GET'])(ActividadController.get_by_id)  # Obtener actividad por ID
actividades_bp.route('/<int:id_actividad>', methods=['PUT'])(ActividadController.update)  # Actualizar actividad
actividades_bp.route('/<int:id_actividad>', methods=['DELETE'])(ActividadController.delete)  # Eliminar actividad
