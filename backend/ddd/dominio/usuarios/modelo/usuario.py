# ddd/dominio/usuarios/modelo/usuario.py

# CLEAN CODE: La clase representa un concepto único (Usuario) y sus atributos.
# DDD: Esta es nuestra Entidad principal en el subdominio de autenticación.

from mongoengine import Document, StringField, EmailField, UUIDField
from uuid import uuid4


class Usuario(Document):
    """
    Entidad de dominio que representa a un Usuario en el sistema.

    Actúa como el 'Aggregate Root' para el agregado de Usuario.
    Hereda de Document para el mapeo directo a MongoDB (Infraestructura).
    """

    id = UUIDField(primary_key=True, default=uuid4)
    nombre = StringField(required=True, max_length=150)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    meta = {
        "collection": "usuarios",
        "indexes": ["email"],
    }
    
    def __init__(self, nombre, email, password, *args, **kwargs):
        """
        Inicializa la entidad Usuario.

        Realiza la validación de los invariantes de creación.
        """
        # INVARIANTE: El nombre no puede ser nulo o vacío (Test 01)
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del usuario no puede ser vacío")
            
        # INVARIANTE: El email debe ser válido
        if not email or "@" not in email:
            raise ValueError("Email inválido.")

        # Llama al constructor de MongoEngine para inicializar los campos
        super().__init__(nombre=nombre, email=email, password=password, *args, **kwargs)

    def actualizar_email(self, nuevo_email: str):
        """
        Método de Comportamiento: Actualiza el correo electrónico del usuario.

        Lanza un ValueError si el nuevo email no cumple con el invariante.
        """
        # INVARIANTE en el Comportamiento (Test 05)
        if not nuevo_email or "@" not in nuevo_email:
            raise ValueError("Email inválido.")
            
        # Comportamiento: Cambiar el estado (Test 04)
        self.email = nuevo_email

    def a_diccionario(self):
        """
        Convierte la entidad a un diccionario para transferencia de datos.

        Returns:
            dict: Un diccionario con los datos públicos del usuario.
        """
        return {
            "id": str(self.id),
            "nombre": str(self.nombre),
            "email": str(self.email),
        }
