from flask import Blueprint, request
from src.controllers.employee_controller_revisar import (
    get_employees_controller,
    add_employee_controller,
    get_employee_by_id_controller,
    update_employee_controller,
    delete_employee_controller,
    employee_login_controller
)

# Definimos el Blueprint para las rutas de empleados
employee_routes_bp = Blueprint("employee_routes", __name__, url_prefix="/empleados")

# Obtener todos los empleados
# Método: GET
# URL: /empleados
employee_routes_bp.route("/", methods=["GET"])(get_employees_controller)

# Agregar un nuevo empleado
# Método: POST
# URL: /empleados
# Body JSON: {"nombre": "Juan", "apellido": "Perez", "email": "juan@empresa.com", "password": "123456", ...}
@employee_routes_bp.route("/", methods=["POST"])
def add_employee():
    data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
    return add_employee_controller(data)

# Obtener un empleado por ID
# Método: GET
# URL: /empleados/{employee_id}
employee_routes_bp.route("/<int:employee_id>", methods=["GET"])(get_employee_by_id_controller)

# Actualizar un empleado por ID
# Método: PUT
# URL: /empleados/{employee_id}
# Body JSON: {"nombre": "Juan", "apellido": "Perez", "email": "juan@empresa.com", "telefono": "123456", ...}
@employee_routes_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
    return update_employee_controller(employee_id, data)
# Eliminar un empleado por ID
# Método: DELETE
# URL: /empleados/{employee_id}
employee_routes_bp.route("/<int:employee_id>", methods=["DELETE"])(delete_employee_controller)

# Login de un empleado
# Método: POST
# URL: /empleados/login
# Body JSON: {"email": "juan@empresa.com", "password": "123456"}
@employee_routes_bp.route("/login", methods=["POST"])
def login_employee():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud
    return employee_login_controller(data)  # Pasar los datos al controlador