def get_all_activities(db):
    """Obtener todas las actividades con precios."""
    query = """
    SELECT a.id, a.nombre, a.dias_habilitados, TIME_FORMAT(a.horario, '%H:%i') as horario, 
           a.sesiones_por_mes, a.max_participantes, a.participantes_actuales, a.activo, cp.precio
    FROM actividades a
    LEFT JOIN configuracion_precios cp ON a.id = cp.referencia_id AND cp.tipo = 'actividad'
    """
    return db.execute_query(query)

def get_activity_by_id(db, activity_id):
    """Obtener los detalles de una actividad específica con su precio."""
    query = """
    SELECT a.id, a.nombre, a.dias_habilitados, TIME_FORMAT(a.horario, '%H:%i') as horario, 
           a.sesiones_por_mes, a.max_participantes, a.participantes_actuales, a.activo, cp.precio
    FROM actividades a
    LEFT JOIN configuracion_precios cp ON a.id = cp.referencia_id AND cp.tipo = 'actividad'
    WHERE a.id = %s
    """
    result = db.execute_query(query, (activity_id,))
    return result[0] if result else None

def create_activity(db, data):
    """Agregar una nueva actividad con su precio."""
    query = """
    INSERT INTO actividades (nombre, dias_habilitados, horario, sesiones_por_mes, max_participantes, participantes_actuales, activo)
    VALUES (%s, %s, %s, %s, %s, 0, True)
    """
    activity_id = db.execute_insert(query, (data["nombre"], data["dias_habilitados"], data["horario"], data["sesiones_por_mes"], data["max_participantes"]))

    price_query = "INSERT INTO configuracion_precios (tipo, referencia_id, precio) VALUES ('actividad', %s, %s)"
    db.execute_update(price_query, (activity_id, data["precio"]))

    return activity_id

def update_activity_by_id(db, activity_id, data):
    """Actualizar una actividad existente."""
    query = """
    UPDATE actividades
    SET nombre = %s, dias_habilitados = %s, horario = %s, sesiones_por_mes = %s, max_participantes = %s
    WHERE id = %s
    """
    rows_affected = db.execute_update(query, (data["nombre"], data["dias_habilitados"], data["horario"], data["sesiones_por_mes"], data["max_participantes"], activity_id))

    if "precio" in data:
        price_query = "UPDATE configuracion_precios SET precio = %s, fecha_actualizacion = CURRENT_TIMESTAMP WHERE tipo = 'actividad' AND referencia_id = %s"
        db.execute_update(price_query, (data["precio"], activity_id))

    return rows_affected > 0

def enroll_member(db, socio_id, actividad_id):
    """Inscribir a un socio en una actividad."""
    check_query = "SELECT id FROM inscripciones WHERE socio_id = %s AND actividad_id = %s"
    existing = db.execute_query(check_query, (socio_id, actividad_id))
    if existing:
        return {"error": "El socio ya está inscrito en esta actividad."}

    query = "INSERT INTO inscripciones (socio_id, actividad_id, sesiones_restantes, fecha_inscripcion) VALUES (%s, %s, (SELECT sesiones_por_mes FROM actividades WHERE id = %s), NOW())"
    db.execute_update(query, (socio_id, actividad_id, actividad_id))

    return {"message": "Inscripción exitosa."}

def unenroll_member(db, socio_id, actividad_id):
    """Desinscribir a un socio de una actividad."""
    delete_query = "DELETE FROM inscripciones WHERE socio_id = %s AND actividad_id = %s"
    db.execute_update(delete_query, (socio_id, actividad_id))
    return {"message": "Desinscripción exitosa."}

def get_activities_by_member(db, socio_id):
    """Obtener actividades en las que está inscrito un socio."""
    query = """
    SELECT a.id, a.nombre FROM inscripciones i JOIN actividades a ON i.actividad_id = a.id WHERE i.socio_id = %s
    """
    return db.execute_query(query, (socio_id,))
