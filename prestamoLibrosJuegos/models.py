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
            raise ValidationError({"rut": "El RUT ingresado no es válido."})

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


# Modelo Prestamo
class Prestamo(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID automático y secuencial

    alumno = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name="prestamos"
    )
    fecha_prestamo = models.DateTimeField(default=now)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    # AlementoDAE no se crea en la base de datos por lo cual daría error en caso de hacer esta relación
    # elemento = models.ForeignKey(
    #     ElementoDAE,  # Relación genérica para libros y juegos
    #     on_delete=models.CASCADE,
    #     related_name="prestamos",
    # )
    # Conviene crear este tipo de relación
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    elemento = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["fecha_prestamo"]),
            models.Index(fields=["fecha_devolucion"]),
            models.Index(fields=["alumno", "elemento"]),
            models.Index(fields=["alumno"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["elemento", "alumno"],
                name="unique_prestamo_activo",
                condition=models.Q(fecha_devolucion__isnull=True),
            )
        ]

    def devolver(self):
        """Marca el préstamo como devuelto"""
        if self.fecha_devolucion:
            raise ValidationError("Este préstamo ya fue devuelto.")

        # Marcar elemento como no prestado
        self.elemento.devolver()

        # Registrar la fecha de devolución
        self.fecha_devolucion = now()
        self.save()

        # Registrar en el historial
        HistorialPrestamos.objects.create(
            alumno=self.alumno,
            elemento=self.elemento,
            fecha_prestamo=self.fecha_prestamo,
            fecha_devolucion=self.fecha_devolucion,
        )

    # Calcular cuanto queda para que finalize el prestamo
    @property
    def duracion(self):
        if self.fecha_devolucion:
            return (self.fecha_devolucion - self.fecha_prestamo).days
        return (now() - self.fecha_prestamo).days

    def __str__(self):
        return f"Préstamo: {self.elemento} a {self.alumno} el {self.fecha_prestamo.strftime('%d/%m/%Y')}"


# Modelo HistorialPrestamos
class HistorialPrestamos(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID automático y secuencial
    alumno = models.ForeignKey(
        Alumno, on_delete=models.SET_NULL, null=True, related_name="historial_prestamos"
    )
    elemento = models.ForeignKey(
        ElementoDAE,
        on_delete=models.SET_NULL,
        null=True,
        related_name="historial_prestamos",
    )
    fecha_prestamo = models.DateTimeField()
    fecha_devolucion = models.DateTimeField()

    def __str__(self):
        return (
            f"Historial: {self.elemento} de {self.alumno} "
            f"({self.fecha_prestamo.strftime('%d/%m/%Y')} - {self.fecha_devolucion.strftime('%d/%m/%Y')})"
        )
