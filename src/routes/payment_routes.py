from flask import Blueprint
from src.controllers.payment_controller import (
    listar_precios,
    obtener_precio_endpoint,
    actualizar_precio_endpoint,
    pagar_cuota,
    obtener_ultimo_pago_por_socio
)

# Definimos el Blueprint para las rutas de pagos
payment_routes_bp = Blueprint("payment_routes", __name__, url_prefix="/pagos")


# Obtener todos los precios disponibles
# Método: GET
# URL: /pagos/precios
payment_routes_bp.route("/precios", methods=["GET"])(listar_precios)

# Obtener el precio de un tipo específico (ej cuota )
# Método: GET
# URL: /pagos/precios/{tipo}
payment_routes_bp.route("/precios/<string:tipo>", methods=["GET"])(obtener_precio_endpoint)

# Actualizar el precio de un tipo de servicio(cuota)
# Método: PUT
# URL: /pagos/precios/cuota
# Body JSON: {"precio": 600}
payment_routes_bp.route("/precios/<string:tipo>", methods=["PUT"])(actualizar_precio_endpoint)

# Registrar el pago de una cuota revisar-------------
# Método: POST
# URL: /pagos/pagar_cuota
# Body JSON: {"socio_id": 1}
payment_routes_bp.route("/pagar_cuota", methods=["POST"])(pagar_cuota)

# Obtener el último pago de un socio
# Método: GET
# URL: /pagos/ultimo_pago/{socio_id}
payment_routes_bp.route("/ultimo_pago/<int:socio_id>", methods=["GET"])(obtener_ultimo_pago_por_socio)
