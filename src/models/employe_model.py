from flask import current_app
import bcrypt
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Para obtener todos los empleados
def get_employees():
    try:
        return current_app.db.execute_query("SELECT * FROM empleados")
    except Exception as e:
        raise Exception(f"Error al obtener empleados: {str(e)}")

# Para agregar un nuevo empleado
def add_employee(data):
    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    query = """
    INSERT INTO empleados (nombre, apellido, email, telefono, direccion, puesto, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data["nombre"], data["apellido"], data["email"],
        data.get("telefono"), data.get("direccion"), data["puesto"], generate_password_hash(data.get("password"))
    )
    try:
        current_app.db.execute_update(query, params)
    except Exception as e:
        raise Exception(f"Error al agregar empleado: {str(e)}")

# Para obtener un empleado por su ID
def get_employee_by_id(employee_id):
    query = "SELECT * FROM empleados WHERE id = %s"
    result = current_app.db.execute_query(query, (employee_id,))
    if not result:
        raise Exception("Empleado no encontrado")
    return result[0]

# Para actualizar un empleado
def update_employee(employee_id, data):
    query = """
    UPDATE empleados
    SET nombre = %s, apellido = %s, email = %s, telefono = %s, direccion = %s, puesto = %s, password = %s
    WHERE id = %s
    """
    params = (
        data["nombre"], data["apellido"], data["email"], 
        data.get("telefono"), data.get("direccion"), data["puesto"], generate_password_hash(data.get("password")), employee_id
    )
    try:
        current_app.db.execute_update(query, params)
    except Exception as e:
        raise Exception(f"Error al actualizar empleado: {str(e)}")

# Para eliminar un empleado
def delete_employee(employee_id):
    query = "DELETE FROM empleados WHERE id = %s"
    try:
        current_app.db.execute_update(query, (employee_id,))
    except Exception as e:
        raise Exception(f"Error al eliminar empleado: {str(e)}")

def verify_employee_login(email, password):
    # Consulta para obtener los detalles del empleado por email
    query = "SELECT id, password FROM empleados WHERE email = %s"
    result = current_app.db.execute_query(query, (email,))

    if not result:
        raise Exception("Empleado no encontrado")

    # Obtener los detalles del empleado y la contraseña almacenada
    employee = result[0]
    stored_password_hash = employee['password']

    # Verificar si la contraseña ingresada coincide con el hash almacenado
    if   check_password_hash(employee["password"], password):
        # Si la contraseña es correcta, devolver el id del empleado
        return  employee
    else:
        raise Exception("Contraseña incorrecta")
# Generar token para el login
