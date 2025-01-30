from flask import jsonify
from src.models.employe_model import get_employees, add_employee, get_employee_by_id, update_employee, delete_employee, verify_employee_login

# Controlador para obtener empleados
def get_employees_controller():
    try:
        employees = get_employees()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador para agregar un nuevo empleado
def add_employee_controller(data):
    try:
        add_employee(data)
        return jsonify({"message": "Empleado agregado exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador para ver un empleado por ID
def get_employee_by_id_controller(employee_id):
    try:
        employee = get_employee_by_id(employee_id)
        return jsonify(employee), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador para actualizar un empleado
def update_employee_controller(employee_id, data):
    try:
        update_employee(employee_id, data)
        return jsonify({"message": "Empleado actualizado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador para eliminar un empleado
def delete_employee_controller(employee_id):
    try:
        delete_employee(employee_id)
        return jsonify({"message": "Empleado eliminado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador para login de un empleado
def employee_login_controller(data):
    try:
        # Verificar que los datos de email y password estén presentes
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Faltan credenciales"}), 400  # Si faltan datos

        # Verificar las credenciales del empleado
        employee = verify_employee_login(email, password)

        if employee:
            # Si el login es exitoso, devolver el id del empleado
            return jsonify({"message": "Login exitoso", "employee_id": employee['id']}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401  # Si las credenciales son incorrectas

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Devuelve un error genérico si algo sale mal

