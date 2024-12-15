from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


# Modelo Alumno
class Alumno(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # Ejemplo: "12345678-9"
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"


# Modelo Libro
class Libro(models.Model):
    nombre = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    prestado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.autor}"


# Modelo JuegoDeMesa
class JuegoDeMesa(models.Model):
    nombre = models.CharField(max_length=100)
    prestado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


# Modelo Prestamo
class Prestamo(models.Model):
    ELEMENTO_CHOICES = (
        ("libro", "Libro"),
        ("juego", "Juego de Mesa"),
    )

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    elemento_tipo = models.CharField(max_length=10, choices=ELEMENTO_CHOICES)
    elemento_id = (
        models.PositiveIntegerField()
    )  # Guarda el ID del elemento (libro o juego)

    def clean(self):
        # Validación: fecha de término no puede ser antes de la fecha de inicio
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError(
                "La fecha de término no puede ser anterior a la fecha de inicio."
            )

        # Validación: Verificar que el elemento no esté prestado
        if self.elemento_tipo == "libro":
            libro = Libro.objects.get(id=self.elemento_id)
            if libro.prestado:
                raise ValidationError(f"El libro '{libro.nombre}' ya está prestado.")
        elif self.elemento_tipo == "juego":
            juego = JuegoDeMesa.objects.get(id=self.elemento_id)
            if juego.prestado:
                raise ValidationError(
                    f"El juego de mesa '{juego.nombre}' ya está prestado."
                )

    def save(self, *args, **kwargs):
        # Sobrescribir save para marcar como prestado
        self.clean()  # Ejecutar validaciones antes de guardar
        if self.elemento_tipo == "libro":
            libro = Libro.objects.get(id=self.elemento_id)
            libro.prestado = True
            libro.save()
        elif self.elemento_tipo == "juego":
            juego = JuegoDeMesa.objects.get(id=self.elemento_id)
            juego.prestado = True
            juego.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Préstamo - {self.alumno} ({self.elemento_tipo.capitalize()}: {self.elemento_id})"
