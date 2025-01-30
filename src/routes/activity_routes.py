from flask import Blueprint
from src.controllers.activity_controller import (
    get_activities, add_activity, get_activity, update_activity, 
    enroll_activity, unenroll_activity, get_enrolled_activities
)

# Definimos el Blueprint para las rutas de actividades
activity_routes_bp = Blueprint("activity_routes", __name__, url_prefix="/actividades")

# Obtener todas las actividades con precios
# Método: GET
# URL: /actividades/
activity_routes_bp.route("/", methods=["GET"])(get_activities)

# Agregar una nueva actividad con precio
# Método: POST
# URL: /actividades/
# Body JSON: {"nombre": "Yoga", "dias_habilitados": "Lunes, Miércoles", "horario": "18:00", "sesiones_por_mes": 8, "max_participantes": 20, "precio": 500}
activity_routes_bp.route("/", methods=["POST"])(add_activity)

# Obtener una actividad por su ID con precio---
# Método: GET
# URL: /actividades/{activity_id}
activity_routes_bp.route("/<int:activity_id>", methods=["GET"])(get_activity)

# Actualizar una actividad existente (incluyendo el precio)---
# Método: PUT
# URL: /actividades/{activity_id}
# Body JSON: {"nombre": "Cycle", "dias_habilitados": "Martes, Jueves", "horario": "19:00", "sesiones_por_mes": 10, "max_participantes": 15, "precio": 600}
activity_routes_bp.route("/<int:activity_id>", methods=["PUT"])(update_activity)

# Inscribir a un socio en una actividad---
# Método: POST
# URL: /actividades/inscripcion
# Body JSON: {"socio_id": 1, "actividad_id": 2}
activity_routes_bp.route("/inscripcion", methods=["POST"])(enroll_activity)

# Desinscribir a un socio de una actividad---
# Método: POST
# URL: /actividades/desinscripcion
# Body JSON: {"socio_id": 1, "actividad_id": 2}
activity_routes_bp.route("/desinscripcion", methods=["POST"])(unenroll_activity)

# Obtener actividades en las que está inscrito un socio---
# Método: GET
# URL: /actividades/inscripciones/{socio_id}
activity_routes_bp.route("/inscripciones/<int:socio_id>", methods=["GET"])(get_enrolled_activities)
