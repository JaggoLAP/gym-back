from flask import jsonify, request, current_app
from ..models.activity_model import (
    get_all_activities, get_activity_by_id, create_activity, update_activity_by_id, 
    enroll_member, unenroll_member, get_activities_by_member
)

def get_activities():
    """Obtener todas las actividades con sus precios."""
    try:
        activities = get_all_activities(current_app.db)
        return jsonify(activities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_activity(activity_id):
    """Obtener una actividad por su ID."""
    try:
        activity = get_activity_by_id(current_app.db, activity_id)
        if not activity:
            return jsonify({"message": "Actividad no encontrada."}), 404
        return jsonify(activity), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_activity():
    """Agregar una nueva actividad."""
    data = request.json
    try:
        activity_id = create_activity(current_app.db, data)
        return jsonify({"message": "Actividad agregada exitosamente.", "id": activity_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_activity(activity_id):
    """Actualizar una actividad existente."""
    data = request.json
    try:
        updated = update_activity_by_id(current_app.db, activity_id, data)
        if not updated:
            return jsonify({"message": "Actividad no encontrada o sin cambios."}), 404
        return jsonify({"message": "Actividad actualizada exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def enroll_activity():
    """Inscribir a un socio en una actividad."""
    data = request.json
    try:
        result = enroll_member(current_app.db, data["socio_id"], data["actividad_id"])
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def unenroll_activity():
    """Desinscribir a un socio de una actividad."""
    data = request.json
    try:
        result = unenroll_member(current_app.db, data["socio_id"], data["actividad_id"])
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_enrolled_activities(socio_id):
    """Obtener actividades en las que está inscrito un socio."""
    try:
        activities = get_activities_by_member(current_app.db, socio_id)
        if not activities:
            return jsonify({"message": "No pertenece a ninguna actividad."}), 200
        return jsonify(activities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
