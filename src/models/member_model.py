from werkzeug.security import generate_password_hash

class MemberModel:
    @staticmethod
    def get_all_members(db):
        query = "SELECT * FROM socios"
        return db.execute_query(query)
    
    @staticmethod
    def get_member_by_id(db, socio_id):
        query = "SELECT * FROM socios WHERE id = %s"
        return db.execute_query(query, (socio_id,))
    
    @staticmethod
    def create_member(db, data):
        query = """
        INSERT INTO socios (nombre, apellido, email, telefono, direccion, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data["nombre"], 
            data["apellido"], 
            data["email"], 
            data.get("telefono"), 
            data.get("direccion"), 
            generate_password_hash(data.get("password"))
        )
        return db.execute_update(query, params)
    
    @staticmethod
    def delete_member(db, socio_id):
        query = "DELETE FROM socios WHERE id = %s"
        return db.execute_update(query, (socio_id,))
    
    @staticmethod
    def update_member(db, socio_id, data):
        query = """
        UPDATE socios
        SET nombre = %s, apellido = %s, email = %s, telefono = %s, direccion = %s
        WHERE id = %s
        """
        params = (
            data["nombre"], 
            data["apellido"], 
            data["email"], 
            data.get("telefono"), 
            data.get("direccion"), 
            socio_id
        )
        return db.execute_update(query, params)
    
    @staticmethod
    def get_member_activities(db, socio_id):
        query = """
        SELECT a.id, a.nombre, a.dias_habilitados, a.horario, a.precio
        FROM inscripciones i
        INNER JOIN actividades a ON i.actividad_id = a.id
        WHERE i.socio_id = %s
        """
        return db.execute_query(query, (socio_id,))
