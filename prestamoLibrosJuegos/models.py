from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(
        max_length=255,
        help_text="Ingresa un nombre de al menos 3 caracteres.",
        error_messages={"min_length": "El nombre debe tener al menos 3 caracteres."},
    )
    telefono = models.CharField(
        max_length=20,
        help_text="Ingresa un teléfono de al menos 7 caracteres.",
        error_messages={"min_length": "El teléfono debe tener al menos 7 caracteres."},
    )
    fecha_ingreso = models.DateField(
        help_text="Seleccione la fecha de ingreso en formato DD/MM/AAAA.",
    )

    def __str__(self):
        return self.nombre
