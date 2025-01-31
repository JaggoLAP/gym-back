import pytest
from src.models.member_model import Socio

@pytest.fixture
def setup_socio_para_baja():
    """Crea un socio temporalmente para probar su eliminación."""
    socio = Socio(nombre="Baja", apellido="Test", email="baja@test.com", estado_membresia="activo")
    Socio.create(socio)
    yield socio  # Devuelve el socio para la prueba

def test_baja_socio(setup_socio_para_baja):
    """Verifica que el socio se elimine correctamente."""
    socio = setup_socio_para_baja

    # Eliminar socio
    resultado = Socio.delete(socio.id)
    
    # Intentar obtenerlo nuevamente
    socio_eliminado = Socio.get_by_id(socio.id)
    
    assert resultado == True, "El método delete no devolvió True"
    assert socio_eliminado is None, "El socio aún existe en la base de datos después de ser eliminado"
