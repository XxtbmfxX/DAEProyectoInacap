from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from datetime import date

from itertools import cycle


def validar_rut(rut):
    rut = rut.upper().replace("-", "").replace(".", "")
    rut_aux = rut[:-1]
    dv = rut[-1:]

    if not rut_aux.isdigit() or not (1_000_000 <= int(rut_aux) <= 25_000_000):
        return False

    revertido = map(int, reversed(rut_aux))
    factors = cycle(range(2, 8))
    suma = sum(d * f for d, f in zip(revertido, factors))
    residuo = suma % 11

    if dv == "K":
        return residuo == 1
    if dv == "0":
        return residuo == 11
    return residuo == 11 - int(dv)


# Clase base para elementos comunes (libros y juegos)
class ElementoDAE(models.Model):
    nombre = models.CharField(max_length=100)
    prestado = models.BooleanField(default=False)

    class Meta:
        abstract = True  # Define que esta clase es abstracta (no crea tabla en la BD)

    def prestar(self):
        if self.prestado:
            raise ValidationError(f"El elemento '{self.nombre}' ya está prestado.")
        self.prestado = True
        self.save()

    def devolver(self):
        self.prestado = False
        self.save()

    def __str__(self):
        return self.nombre


# Modelo Alumno
class Alumno(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def clean(self):
        # Validar el RUT
        if not validar_rut(self.rut):
            raise ValidationError("El RUT ingresado no es válido.")

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"


# Modelo Libro, hereda de ElementoDAE
class Libro(ElementoDAE):
    autor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.autor}"


# Modelo JuegoDeMesa, hereda de ElementoDAE
class JuegoDeMesa(ElementoDAE):
    pass


# Modelo Prestamo usando GenericForeignKey
class Prestamo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    elemento = GenericForeignKey("content_type", "object_id")

    def clean(self):
        # Validar que la fecha de término no sea anterior a la de inicio
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError(
                "La fecha de término no puede ser anterior a la fecha de inicio."
            )

        # Validar que el elemento no esté prestado
        if self.elemento.prestado:
            raise ValidationError(
                f"El elemento '{self.elemento.nombre}' ya está prestado."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Ejecuta las validaciones
        self.elemento.prestar()  # Marca el elemento como prestado
        super().save(*args, **kwargs)

    def devolver(self):
        # Marca el elemento como devuelto y guarda el historial
        self.elemento.devolver()
        HistorialPrestamos.objects.create(
            alumno=self.alumno,
            fecha_inicio=self.fecha_inicio,
            fecha_termino=self.fecha_termino,
            content_type=self.content_type,
            object_id=self.object_id,
        )
        self.delete()

    def __str__(self):
        return f"Préstamo - {self.alumno} ({self.elemento})"


# Modelo HistorialPrestamos
class HistorialPrestamos(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    elemento = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Historial - {self.alumno} ({self.elemento})"
