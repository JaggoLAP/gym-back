from flask import current_app

def obtener_conexion():
    """Obtiene una conexión a la base de datos desde la app actual."""
    return current_app.db.get_connection()

def obtener_todos_los_precios():
    """Obtiene todos los precios de la tabla configuracion_precios."""
    connection = obtener_conexion()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuracion_precios")
    precios = cursor.fetchall()
    cursor.close()
    return precios

def obtener_precio(tipo, referencia_id=None):
    """Obtiene un precio específico filtrado por tipo y referencia_id."""
    connection = obtener_conexion()
    cursor = connection.cursor(dictionary=True)

    try:
        if referencia_id:
            query = "SELECT * FROM configuracion_precios WHERE tipo = %s AND referencia_id = %s"
            cursor.execute(query, (tipo, referencia_id))
        else:
            query = "SELECT * FROM configuracion_precios WHERE tipo = %s AND referencia_id IS NULL"
            cursor.execute(query, (tipo,))

        precios = cursor.fetchall()
        return precios[0] if precios else None
    except Exception as e:
        print(f"Error al obtener el precio: {e}")
        return None
    finally:
        cursor.close()

def actualizar_precio(tipo, referencia_id, nuevo_precio):
    """Actualiza el precio de un registro en configuracion_precios."""
    connection = obtener_conexion()
    cursor = connection.cursor()
    
    if referencia_id:
        query = "UPDATE configuracion_precios SET precio = %s WHERE tipo = %s AND referencia_id = %s"
        cursor.execute(query, (nuevo_precio, tipo, referencia_id))
    else:
        query = "UPDATE configuracion_precios SET precio = %s WHERE tipo = %s AND referencia_id IS NULL"
        cursor.execute(query, (nuevo_precio, tipo))
    
    connection.commit()
    filas_actualizadas = cursor.rowcount
    cursor.close()
    return filas_actualizadas > 0
