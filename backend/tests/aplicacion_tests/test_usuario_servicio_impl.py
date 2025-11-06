import pytest
from unittest.mock import Mock, MagicMock
from ddd.aplicacion.usuario_servicio_impl import UsuarioServicioImpl 
from ddd.dominio.usuarios.modelo.usuario import Usuario
from ddd.aplicacion.dto import CrearUsuarioDTO, UsuarioDTO 


# ARRANGE: Mocks de dependencias(dobles de prueba)

@pytest.fixture
def usuario_mock_entidad():
    """Entidad Usuario simulada, con atributos concretos para las aserciones."""
    # Se crea una Entidad de Dominio real para ser usada por los mocks
    return Usuario(id="123", nombre="Alice", email="alice@test.com", password="hash")

@pytest.fixture
def mock_repo(usuario_mock_entidad):
    """Mock para la interfaz UsuarioRepositorio, simulando la persistencia."""
    mock = MagicMock()
    # Configurar el Mock para devolver la entidad concreta al ser guardada
    mock.guardar.return_value = usuario_mock_entidad 
    return mock

@pytest.fixture
def mock_fabrica(usuario_mock_entidad):
    """Mock para la interfaz UsuarioFabrica."""
    mock = MagicMock()
    # Configurar el Mock para devolver la entidad concreta al ser creada
    mock.crear_usuario.return_value = usuario_mock_entidad 
    return mock

@pytest.fixture
def mock_servicio_hash():
    """Mock para el ServicioHash."""
    return Mock()

# --- ARRANGE: DATOS DE ENTRADA ---

@pytest.fixture
def crear_dto():
    """DTO de entrada para el caso de uso 'crear_usuario'."""
    return CrearUsuarioDTO(nombre="Alice", email="alice@test.com", password="pwd")


# PRUEBAS DE INTEGRACIÓN: CASO DE USO crear_usuario 

def test_crear_usuario_caso_exitoso_orquesta_y_guarda(
    mock_repo, mock_fabrica, mock_servicio_hash, crear_dto
):
    """
    Verifica que el servicio orquesta correctamente las llamadas a sus dependencias
    (Fabrica y Repositorio) cuando el caso de uso es exitoso.
    """
    # Arrange: Configurar el Repositorio (Mock)
    mock_repo.existe_email.return_value = False # Simular que el email es único
    
    # Arrange: Inicializar el SUT (Servicio) inyectando los Mocks
    servicio = UsuarioServicioImpl(
        usuario_repositorio=mock_repo, 
        usuario_fabrica=mock_fabrica, 
        servicio_hash=mock_servicio_hash
    )
    
    # Act: Ejecutar el método bajo prueba
    resultado_dto = servicio.crear_usuario(crear_dto)
    
    # Assert: Verificar la Orquestación y el Resultado
    
    # El servicio debe verificar la existencia del email
    mock_repo.existe_email.assert_called_once_with(crear_dto.email)
    
    # El servicio debe usar la fábrica
    mock_fabrica.crear_usuario.assert_called_once()
    
    # El servicio debe guardar la entidad
    mock_repo.guardar.assert_called_once()
    
    # Verificar que retorna el DTO correcto
    assert isinstance(resultado_dto, UsuarioDTO)
    assert resultado_dto.email == crear_dto.email


def test_crear_usuario_falla_si_el_email_ya_existe(
    mock_repo, mock_fabrica, mock_servicio_hash, crear_dto
):
    """
    Verifica que el servicio lance una excepción si el email ya está registrado
    y que la creación/guardado no ocurran.
    """
    # Arrange: Configurar el Mock para el Fallo
    mock_repo.existe_email.return_value = True # Simular que el email SÍ existe
    
    # Arrange: Inicializar el SUT
    servicio = UsuarioServicioImpl(
        usuario_repositorio=mock_repo, 
        usuario_fabrica=mock_fabrica, 
        servicio_hash=mock_servicio_hash
    )
    
    # Act & Assert: Esperar la excepción de negocio (ValueError)
    with pytest.raises(ValueError) as excinfo:
        servicio.crear_usuario(crear_dto)
        
    # Assert: Verificar la Interacción
    
    # Se debe verificar la existencia
    mock_repo.existe_email.assert_called_once()
    
    # Los métodos de creación y guardado NO DEBEN llamarse
    mock_fabrica.crear_usuario.assert_not_called()
    mock_repo.guardar.assert_not_called()
    
    # Verificar el mensaje de error
    assert "El email ya está en uso." in str(excinfo.value)
