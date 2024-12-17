from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from itertools import cycle
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def validar_rut(rut):
    rut = rut.upper().replace("-", "").replace(".", "")
    rut_aux = rut[:-1]
    dv = rut[-1:]

    if not rut_aux.isdigit() or not (1_000_000 <= int(rut_aux) <= 25_000_000):
        raise ValidationError("El RUT ingresado no tiene un formato válido.")

    revertido = map(int, reversed(rut_aux))
    factors = cycle(range(2, 8))
    suma = sum(d * f for d, f in zip(revertido, factors))
    residuo = suma % 11

    if dv == "K" and residuo == 1:
        return
    if dv == "0" and residuo == 11:
        return
    if residuo != 11 - int(dv):
        raise ValidationError("El RUT ingresado no es válido.")


# Modelo Alumno
class Alumno(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    # def clean(self):
    #     # Validar el RUT
    #     if not validar_rut(self.rut):
    #         raise ValidationError({"rut": "El RUT ingresado no es válido."})

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    prestado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo}"


class JuegoDeMesa(models.Model):
    nombre = models.CharField(max_length=255)
    prestado = models.BooleanField(default=False)
    # jugadores = models.IntegerField()

    def __str__(self):
        return f"{self.nombre}"


# Modelo Prestamo
class Prestamo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()

    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True, blank=True)
    juego = models.ForeignKey(
        JuegoDeMesa, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(libro__isnull=False, juego__isnull=False),
                name="no_libro_and_juego",
            ),
            models.CheckConstraint(
                check=~models.Q(libro__isnull=True, juego__isnull=True),
                name="at_least_one_item",
            ),
        ]

    def clean(self):
        # Validar que solo un campo esté configurado
        if self.libro and self.juego:
            raise ValidationError(
                "Un préstamo no puede tener un libro y un juego de mesa al mismo tiempo."
            )
        if not self.libro and not self.juego:
            raise ValidationError("Debes seleccionar un libro o un juego de mesa.")

        # Validar préstamos activos
        if self.libro:
            prestamo_activo = Prestamo.objects.filter(
                libro=self.libro, alumno=self.alumno, fecha_termino__isnull=True
            ).exclude(pk=self.pk)
            if prestamo_activo.exists():
                raise ValidationError(
                    "El alumno ya tiene un préstamo activo para este libro."
                )

        if self.juego:
            prestamo_activo = Prestamo.objects.filter(
                juego=self.juego, alumno=self.alumno, fecha_termino__isnull=True
            ).exclude(pk=self.pk)
            if prestamo_activo.exists():
                raise ValidationError(
                    "El alumno ya tiene un préstamo activo para este juego."
                )

    def __str__(self):
        item = self.libro or self.juego
        return f"Préstamo de {item} a {self.alumno}"


# Modelo HistorialPrestamos
class HistorialPrestamos(models.Model):
    alumno = models.ForeignKey(
        Alumno, on_delete=models.SET_NULL, null=True, related_name="historial_prestamos"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    elemento = GenericForeignKey("content_type", "object_id")
    fecha_prestamo = models.DateTimeField()
    fecha_devolucion = models.DateTimeField()

    def __str__(self):
        return (
            f"Historial: {self.elemento} de {self.alumno} "
            f"({self.fecha_prestamo.strftime('%d/%m/%Y')} - {self.fecha_termino.strftime('%d/%m/%Y')})"
        )
