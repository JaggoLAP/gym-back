from ..database import DatabaseConnection

class Actividad:
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nombre = kwargs.get('nombre')
        self.dias_habilitados = kwargs.get('dias_habilitados')
        self.horario = kwargs.get('horario')
        self.sesiones_por_mes = kwargs.get('sesiones_por_mes')
        self.max_participantes = kwargs.get('max_participantes')
        self.participantes_actuales = kwargs.get('participantes_actuales', 0)
        self.precio = kwargs.get('precio')
        self.activo =kwargs.get('activo')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'dias_habilitados': self.dias_habilitados,
            'horario': self.horario.strftime('%H:%M:%S') if self.horario else None,
            'sesiones_por_mes': self.sesiones_por_mes,
            'max_participantes': self.max_participantes,
            'participantes_actuales': self.participantes_actuales,
            'precio': self.precio,
            'activo': self.activo
        }

    @classmethod
    def get_all_disponibles(cls):
        query = """SELECT * FROM gym_management.actividades
                   WHERE participantes_actuales < max_participantes"""
        results = DatabaseConnection.fetch_all(query)
        return [cls(**row) for row in results]
        if result is not None:
            return cls(
                id=result[0],
                nombre=result[1],
                dias_habilitados=result[2],
                horario=result[3],
                sesiones_por_mes=result[4],
                max_participantes=result[5],
                participantes_actuales=result[6],
                precio=result[7],
                activo=result[8]
            )
        else:
            return None


    @classmethod
    def create(cls, actividad):
        query = """INSERT INTO gym_management.actividades (nombre, dias_habilitados, horario, sesiones_por_mes, max_participantes, participantes_actuales, precio, activo)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (actividad.nombre, actividad.dias_habilitados, actividad.horario, actividad.sesiones_por_mes, actividad.max_participantes, actividad.participantes_actuales, actividad.precio, actividad.activo)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update(cls, actividad):
        query = """UPDATE gym_management.actividades
                   SET nombre = %s, dias_habilitados = %s, horario = %s, sesiones_por_mes = %s, max_participantes = %s, participantes_actuales = %s, precio = %s, activo = %s
                   WHERE id = %s"""
        params = (actividad.nombre, actividad.dias_habilitados, actividad.horario, actividad.max_participantes, actividad.participantes_actuales, actividad.id)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def delete(cls, actividad_id):
        query = "DELETE FROM gym_management.actividades WHERE id = %s"
        params = (actividad_id,)
        DatabaseConnection.execute_query(query, params=params)
