from flask import jsonify, request, current_app
from src.models.payment_model import obtener_todos_los_precios, obtener_precio, actualizar_precio
from datetime import datetime, timedelta
from src.db import DbError
from dateutil.relativedelta import relativedelta
def listar_precios():
    """Devuelve todos los precios en formato JSON."""
    precios = obtener_todos_los_precios()
    return jsonify(precios)

def obtener_precio_endpoint(tipo):
    """Endpoint para obtener un precio específico por tipo y referencia_id."""
    referencia_id = request.args.get('referencia_id')
    precio = obtener_precio(tipo, referencia_id)
    if not precio:
        return jsonify({"error": "Precio no encontrado"}), 404
    return jsonify(precio)

def actualizar_precio_endpoint(tipo):
    """Actualiza un precio específico en la base de datos."""
    data = request.json
    referencia_id = data.get('referencia_id')
    nuevo_precio = data.get('precio')

    if nuevo_precio is None:
        return jsonify({"error": "El precio es obligatorio"}), 400

    exito = actualizar_precio(tipo, referencia_id, nuevo_precio)
    if not exito:
        return jsonify({"error": "Precio no encontrado"}), 404

    return jsonify({"message": "Precio actualizado con éxito"})


def _pagar_cuota(db, socio_id):
    try:
        query_monto = """
            SELECT precio FROM configuracion_precios
            WHERE tipo = 'cuota' AND referencia_id IS NULL
            ORDER BY fecha_actualizacion DESC LIMIT 1
        """
        resultado = db.execute_query(query_monto)
        
        if not resultado:
            return {'error': 'No se encontró el precio de la cuota en la configuración'}, 500

        monto_cuota = resultado[0]['precio']

        query = """
            SELECT fecha_fin FROM cuotas
            WHERE socio_id = %s
            ORDER BY id DESC
            LIMIT 1
        """
        ultima_cuota = db.execute_query(query, (socio_id,))
        fecha_hoy = datetime.utcnow().date()
        dias_gracia = 3

        if ultima_cuota:
            fecha_fin_anterior = ultima_cuota[0]['fecha_fin']
            fecha_vencimiento = fecha_fin_anterior + timedelta(days=dias_gracia)

            if fecha_hoy >= fecha_vencimiento:
                dias_restantes = 3 
            else:
                fecha_vencimiento_ajustada  = fecha_vencimiento - timedelta(days=dias_gracia)
                dias_restantes = (fecha_vencimiento_ajustada  - fecha_hoy).days # Restar días de gracia 
        else:
            dias_restantes = 0
        if dias_restantes>3:
            dias_restantes=3
        fecha_inicio = fecha_hoy
        fecha_fin = fecha_inicio + timedelta(days=30 - dias_restantes)

        insert_cuota_query = """
            INSERT INTO cuotas (socio_id, fecha_pago, fecha_inicio, fecha_fin, estado, monto)
            VALUES (%s, %s, %s, %s, 'activa', %s)
        """
        db.execute_update(insert_cuota_query, (socio_id, fecha_hoy, fecha_inicio, fecha_fin, monto_cuota))

        update_socio_query = "UPDATE socios SET estado = 'activo' WHERE id = %s"
        db.execute_update(update_socio_query, (socio_id,))

        return {
            'mensaje': 'Cuota pagada exitosamente',
            'monto': monto_cuota,
            'fecha_fin': fecha_fin.isoformat(),
            'fecha_ini': fecha_inicio.isoformat(),
            'dias de gracia':dias_restantes
        }
    except DbError as e:
        return {'error': str(e)}, 500


def pagar_cuota():
    try:
        data = request.json
        if not data or 'socio_id' not in data:
            return jsonify({'error': 'Se requiere socio_id'}), 400
        
        db = getattr(current_app, 'db', None)
        if db is None:
            return jsonify({'error': 'No se pudo obtener la conexión a la base de datos'}), 500

        return jsonify(_pagar_cuota(db, data['socio_id']))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def obtener_ultimo_pago_por_socio(socio_id):
    """Devuelve el último pago de un socio."""
    try:
        db = current_app.db
        query = """
            SELECT s.estado, c.fecha_fin
            FROM socios s
            JOIN cuotas c ON s.id = c.socio_id
            WHERE s.id = %s
            ORDER BY c.id DESC
            LIMIT 1;
        """
        resultado = db.execute_query(query, (socio_id,))

        if not resultado:
            return jsonify({'error': f'No se encontraron pagos para el socio con ID {socio_id}'}), 404

        return jsonify(resultado[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
