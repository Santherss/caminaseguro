import pytest 
from ddd.dominio.usuarios.modelo.ubicacion import Ubicacion


def test_02_invariante_latitud_fuera_rango_falla():
    """
    PRUEBA 2: Verifica el invariante de latitud.
    Asegura que el Objeto de Valor Ubicacion falle si la latitud está 
    fuera del rango válido (-90 a 90).
    """
    latitud_invalida = 90.01 
    longitud_valida = 0.0

    with pytest.raises(ValueError) as excinfo:
        Ubicacion(latitud=latitud_invalida, longitud=longitud_valida)
    
    assert "La latitud debe estar entre -90 y 90" in str(excinfo.value)
