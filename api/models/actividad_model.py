from ..database import DatabaseConnection

class Actividad:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nombre = kwargs.get('nombre')
        self.dias_habilitados = kwargs.get('dias_habilitados')
        self.horario = kwargs.get('horario')
        self.max_participantes = kwargs.get('max_participantes')
        self.participantes_actuales = kwargs.get('participantes_actuales', 0)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'dias_habilitados': self.dias_habilitados,
            'horario': self.horario.strftime('%H:%M:%S') if self.horario else None,
            'max_participantes': self.max_participantes,
            'participantes_actuales': self.participantes_actuales
        }

    @classmethod
    def get_all_disponibles(cls):
        query = """SELECT * FROM actividades
                   WHERE participantes_actuales < max_participantes"""
        results = DatabaseConnection.fetch_all(query)
        return [cls(**row) for row in results]

    @classmethod
    def create(cls, actividad):
        query = """INSERT INTO actividades (nombre, dias_habilitados, horario, max_participantes, participantes_actuales)
                   VALUES (%s, %s, %s, %s, %s)"""
        params = (actividad.nombre, actividad.dias_habilitados, actividad.horario, actividad.max_participantes, actividad.participantes_actuales)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update(cls, actividad):
        query = """UPDATE actividades
                   SET nombre = %s, dias_habilitados = %s, horario = %s, max_participantes = %s, participantes_actuales = %s
                   WHERE id = %s"""
        params = (actividad.nombre, actividad.dias_habilitados, actividad.horario, actividad.max_participantes, actividad.participantes_actuales, actividad.id)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, actividad_id):
        query = "DELETE FROM actividades WHERE id = %s"
        params = (actividad_id,)
        DatabaseConnection.execute_query(query, params=params)
