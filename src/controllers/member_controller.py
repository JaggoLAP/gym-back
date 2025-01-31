from flask import jsonify
from ..models.member_model import MemberModel

class MemberController:
    @staticmethod
    def get_all_members(db):
        try:
            socios = MemberModel.get_all_members(db)
            return jsonify(socios), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_member(db, socio_id):
        try:
            socio = MemberModel.get_member_by_id(db, socio_id)
            if not socio:
                return jsonify({"message": "Socio no encontrado."}), 404
            return jsonify(socio[0]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_member_by_email(db, email):
        try:
            print('email by controller: ', email)
            socio = MemberModel.get_member_by_email(db, email)
            print('socio by controller: ', socio)
            if not socio:
                return jsonify({"message": "Socio no encontrado."}), 404
            print('json by controller: ', jsonify(socio[0]))
            return jsonify(socio[0]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_member(db, data):
        try:
            MemberModel.create_member(db, data)
            return jsonify({"message": "Socio agregado exitosamente."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_member(db, socio_id):
        try:
            socio = MemberModel.get_member_by_id(db, socio_id)
            if not socio:
                return jsonify({"message": "Socio no encontrado."}), 404
            MemberModel.delete_member(db, socio_id)
            return jsonify({"message": "Socio eliminado exitosamente."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_member(db, socio_id, data):
        try:
            socio = MemberModel.get_member_by_id(db, socio_id)
            if not socio:
                return jsonify({"message": "Socio no encontrado."}), 404
            MemberModel.update_member(db, socio_id, data)
            return jsonify({"message": "Socio actualizado exitosamente."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_activities_by_member(db, socio_id):
        try:
            actividades = MemberModel.get_member_activities(db, socio_id)
            if not actividades:
                return jsonify({"message": "El socio no tiene actividades registradas."}), 404
            return jsonify(actividades), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
