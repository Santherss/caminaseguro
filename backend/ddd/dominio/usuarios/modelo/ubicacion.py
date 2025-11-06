# ddd/dominio/usuarios/modelo/ubicacion.py

from django.db import models

class Ubicacion(models.Model):
    """Objeto de Valor que representa una ubicación geográfica."""
    
    latitud = models.DecimalField()
    longitud = models.DecimalField()
    referencia = models.CharField()

    class Meta:
        pass
        
    def __init__(self, latitud, longitud, referencia=None, *args, **kwargs):
        # INVARIANTE: La latitud debe estar dentro del rango [-90, 90]
        if latitud is not None and (latitud < -90 or latitud > 90):
            raise ValueError("La latitud debe estar entre -90 y 90")
            
        # Llama al constructor de la clase base (models.Model)
        super().__init__(latitud=latitud, longitud=longitud, referencia=referencia, *args, **kwargs)

    def esta_dentro_radio(self, lat, lon, radio_km):
        # Lógica de cálculo de distancia (Comportamiento).
        pass
