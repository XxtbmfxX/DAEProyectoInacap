from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Prestamo, Libro, JuegoDeMesa, Alumno, validar_rut


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["alumno", "elemento", "fecha_prestamo"]
        widgets = {
            "alumno": forms.Select(attrs={"class": "form-control"}),
            "elemento": forms.Select(attrs={"class": "form-control"}),
            "fecha_prestamo": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }
        labels = {
            "alumno": "Alumno",
            "elemento": "Elemento a prestar (Libro o Juego)",
            "fecha_prestamo": "Fecha del préstamo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los elementos disponibles (no prestados)
        # Hacemos un query a la base de datos
        elementos_disponibles = list(Libro.objects.filter(prestado=False)) + list(
            JuegoDeMesa.objects.filter(prestado=False)
        )
        self.fields["elemento"].queryset = elementos_disponibles

    # Validaciones extra
    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get("alumno")
        elemento = cleaned_data.get("elemento")

        if not alumno:
            self.add_error("alumno", "Debe seleccionar un alumno válido.")
        if not elemento:
            self.add_error("elemento", "Debe seleccionar un libro o juego disponible.")


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ["rut", "nombre", "apellido"]
        widgets = {
            "rut": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: 12345678-9"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre"}
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apellido"}
            ),
        }
        labels = {
            "rut": "RUT",
            "nombre": "Nombre",
            "apellido": "Apellido",
        }

    # Validación extra
    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        if rut and not validar_rut(rut):  # Usamos la función validar_rut
            self.add_error("rut", "El RUT ingresado no es válido.")


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["nombre", "autor"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del libro"}
            ),
            "autor": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Autor"}
            ),
        }
        labels = {
            "nombre": "Nombre del libro",
            "autor": "Autor",
        }


class JuegoDeMesaForm(forms.ModelForm):
    class Meta:
        model = JuegoDeMesa
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del juego"}
            ),
        }
        labels = {
            "nombre": "Nombre del juego de mesa",
        }
