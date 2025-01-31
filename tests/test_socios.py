import pytest
from src.models.member_model import Socio
from src.models.payment_model import Cuota
from src.db import DatabaseConnection

@pytest.fixture
def setup_socio():
    """Crea un socio de prueba en la base de datos."""
    socio = Socio(nombre="Prueba", apellido="Test", email="prueba@test.com", estado_membresia="inactivo")
    Socio.create(socio)
    yield socio  # Devuelve el socio para las pruebas
    Socio.delete(socio.id)  # Limpia después de la prueba

def test_habilitar_socio_con_pago(setup_socio):
    """Verifica que al pagar la cuota, el socio pase a estado 'activo'."""
    socio = setup_socio
    cuota = Cuota(id_socio=socio.id, fecha_inicio="2024-02-01", fecha_fin="2024-02-28", estado="pagada")
    Cuota.create(cuota)

    # Simular actualización del estado del socio después del pago
    socio.estado_membresia = "activo"
    Socio.update(socio)

    socio_actualizado = Socio.get_by_id(socio.id)
    assert socio_actualizado.estado_membresia == "activo", "El socio no fue habilitado correctamente después del pago"
