from datetime import datetime, timedelta
import pytest
from src.models.payment_model import Cuota
from src.models.member_model import Socio

@pytest.fixture
def setup_cuota_vencida():
    """Crea un socio con una cuota vencida."""
    socio = Socio(nombre="Deudor", apellido="Test", email="deudor@test.com", estado_membresia="activo")
    Socio.create(socio)

    # Cuota con fecha de vencimiento en el pasado
    cuota = Cuota(id_socio=socio.id, fecha_inicio="2024-01-01", fecha_fin="2024-01-31", estado="pagada")
    Cuota.create(cuota)

    yield socio, cuota
    Socio.delete(socio.id)

def test_vencimiento_cuota(setup_cuota_vencida):
    """Verifica que el socio pase a 'deudor' si su cuota está vencida."""
    socio, cuota = setup_cuota_vencida
    fecha_actual = datetime.strptime("2024-02-05", "%Y-%m-%d")  # Fecha de prueba (después del vencimiento)

    if fecha_actual.date() > datetime.strptime(cuota.fecha_fin, "%Y-%m-%d").date():
        socio.estado_membresia = "deudor"
        Socio.update(socio)

    socio_actualizado = Socio.get_by_id(socio.id)
    assert socio_actualizado.estado_membresia == "deudor", "El socio no fue marcado como 'deudor' tras vencimiento de la cuota"
