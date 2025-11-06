import pytest
from ddd.dominio.usuarios.modelo.usuario import Usuario  
# Se importa la implementación CONCRETA de la infraestructura para el SUT
from ddd.infraestructura.mongodb.mongo_usuario_repositorio import MongoUsuarioRepositorio 


@pytest.fixture
def usuario_ejemplo():
    """Crea una entidad Usuario válida para ser usada en los tests de persistencia."""
    return Usuario(nombre="TestRepo", email="repo@test.com", password="hash_seguro")


def test_guardar_usuario_verifica_la_llamada_al_metodo_save(mocker, usuario_ejemplo):
    """
    Verifica que la implementación del Repositorio llame al método de persistencia
    (save) del objeto MongoEngine, aislando la prueba con Mocking.
    """
    # Arrange: Inicializar el Sistema Bajo Prueba (SUT)
    repositorio = MongoUsuarioRepositorio()
    
    # Arrange: Mocking. Sustituir el método save() del documento por un doble de prueba.
    mock_save = mocker.patch.object(usuario_ejemplo, 'save')

    # Act: Ejecutar el método del Repositorio
    repositorio.guardar(usuario_ejemplo)

    # Assert: Verificar la Interacción. Asegurar que el mock fue llamado una vez.
    mock_save.assert_called_once()
