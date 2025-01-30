

from flask_jwt_extended import create_access_token

from werkzeug.security import check_password_hash

def authenticate_user(email, password, db_connection):
    """
    Autentica al usuario verificando el email y la contraseña.
    """
    cursor = db_connection.cursor()

    # Buscar primero en la tabla de socios
    query_socios = "SELECT id, password, 'socio' AS role FROM socios WHERE email = %s"
    cursor.execute(query_socios, (email,))
    socio = cursor.fetchone()

    if socio:
        print(f"[DEBUG] Socio encontrado: {socio}")  # Verifica qué devuelve la consulta
        print(f"[DEBUG] Hash almacenado: {socio[1]}")
        print(f"[DEBUG] Contraseña ingresada: {password}")

        if check_password_hash(socio[1], password):
            cursor.close()
            return {"id": socio[0], "role": socio[2]}
        else:
            print("[ERROR] Contraseña incorrecta para socio")

    # Si no se encuentra en socios, buscar en la tabla de empleados
    query_empleados = "SELECT id, password, 'empleado' AS role FROM empleados WHERE email = %s"
    cursor.execute(query_empleados, (email,))
    empleado = cursor.fetchone()

    if empleado:
        print(f"[DEBUG] Empleado encontrado: {empleado}")
        print(f"[DEBUG] Hash almacenado: {empleado[1]}")
        print(f"[DEBUG] Contraseña ingresada: {password}")

        if check_password_hash(empleado[1], password):
            cursor.close()
            return {"id": empleado[0], "role": empleado[2]}
        else:
            print("[ERROR] Contraseña incorrecta para empleado")

    cursor.close()
    return None



def generate_token(user):
    """
    Genera un token JWT para el usuario autenticado.
    """
    return create_access_token(identity={"id": user["id"], "role": user["role"]})
