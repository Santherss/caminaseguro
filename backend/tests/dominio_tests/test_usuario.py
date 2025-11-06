import pytest
from ddd.dominio.usuarios.modelo.usuario import Usuario

# Arrange: Datos base para la creación de la entidad Usuario
DATOS_BASE_USUARIO = {
    "nombre": "Ana", 
    "email": "ana.perez@example.com", 
    "password": "hashedpassword123", 
}

# --- PRUEBAS DE INVARIANTES DE CREACIÓN ---

def test_01_invariante_nombre_vacio_falla():
    """
    PRUEBA 1: Verifica el Invariante de Creación (Invalidez).
    Asegura que la entidad falle si el nombre es nulo o vacío.
    """
    # Arrange: Configurar datos inválidos
    nombre_invalido = ""
    datos_prueba = DATOS_BASE_USUARIO.copy()
    datos_prueba["nombre"] = nombre_invalido
    
    # Act & Assert: Verificar que se lanza la excepción (fallo de invariante)
    with pytest.raises(ValueError) as excinfo:
        Usuario(**datos_prueba)
    
    assert "El nombre del usuario no puede ser vacío" in str(excinfo.value)

def test_03_creacion_usuario_exitosa():
    """
    PRUEBA 3: Happy Path.
    Asegura que la entidad se cree y sus atributos se asignen correctamente.
    """
    # Arrange
    nombre_valido = DATOS_BASE_USUARIO["nombre"]
    
    # Act
    usuario = Usuario(**DATOS_BASE_USUARIO)

    # Assert
    assert usuario.nombre == nombre_valido

# --- PRUEBAS DE COMPORTAMIENTO Y SUS INVARIANTES ---

def test_04_actualizar_email_exitoso():
    """
    PRUEBA 4: Verifica el Comportamiento. 
    Asegura que el método de negocio 'actualizar_email' cambie el estado de la entidad.
    """
    # Arrange: Inicializar la entidad y definir el nuevo valor
    usuario = Usuario(**DATOS_BASE_USUARIO)
    nuevo_email_valido = "nuevo.email@caminaseguro.com"
    
    # Act: Ejecutar el comportamiento
    usuario.actualizar_email(nuevo_email_valido) 
    
    # Assert: Verificar el cambio de estado
    assert usuario.email == nuevo_email_valido

def test_05_actualizar_email_invalido_falla():
    """
    PRUEBA 5: Verifica el Invariante en el Comportamiento. 
    Asegura que el método falle si se intenta actualizar con un valor que rompa la regla de negocio.
    """
    # Arrange: Inicializar la entidad y definir el valor inválido
    usuario = Usuario(**DATOS_BASE_USUARIO)
    email_invalido = ""
    
    # Act & Assert: Verificar que se lanza la excepción al intentar cambiar el estado
    with pytest.raises(ValueError) as excinfo:
        usuario.actualizar_email(email_invalido) 
        
    assert "Email inválido." in str(excinfo.value)
