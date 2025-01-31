from flask import Blueprint, request, current_app
from ..controllers.member_controller import MemberController

member_routes_bp = Blueprint("member_routes", __name__, url_prefix="/socios")

@member_routes_bp.route("/", methods=["GET"])
def get_socios():
    return MemberController.get_all_members(current_app.db)

@member_routes_bp.route("/<int:socio_id>", methods=["GET"])
def get_socio(socio_id):
    return MemberController.get_member(current_app.db, socio_id)

@member_routes_bp.route("/email/<string:email>", methods=["GET"])
def get_socio_email(email):
    print('email by routes: ', email)
    return MemberController.get_member_by_email(current_app.db, email)

@member_routes_bp.route("/", methods=["POST"])
def add_socio():
    data = request.json
    print("routes, data!",data)
    return MemberController.create_member(current_app.db, data)

@member_routes_bp.route("/<int:socio_id>", methods=["DELETE"])
def delete_socio(socio_id):
    return MemberController.delete_member(current_app.db, socio_id)

@member_routes_bp.route("/<int:socio_id>", methods=["PUT"])
def update_socio(socio_id):
    data = request.json
    return MemberController.update_member(current_app.db, socio_id, data)

@member_routes_bp.route("/actividades/<int:socio_id>", methods=["GET"])
def get_activities_by_member(socio_id):
    return MemberController.get_activities_by_member(current_app.db, socio_id)
