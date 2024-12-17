from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Prestamo, Libro, JuegoDeMesa, Alumno, validar_rut


class PrestamoForm(forms.ModelForm):
    tipo_elemento = forms.ChoiceField(
        choices=[("libro", "Libro"), ("juego", "Juego de Mesa")],
        label="Tipo de elemento",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    elemento_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Prestamo
        fields = ["alumno", "tipo_elemento", "fecha_inicio"]
        widgets = {
            "alumno": forms.Select(attrs={"class": "form-control"}),
            "fecha_inicio": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "fecha_termino": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }
        labels = {
            "alumno": "Alumno",
            "fecha_inicio": "Fecha de préstamo",
            "fecha_termino": "Fecha de termino",
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_elemento = cleaned_data.get("tipo_elemento")
        alumno = cleaned_data.get("alumno")

        # Validar que el tipo de elemento sea válido
        if tipo_elemento not in ["libro", "juego"]:
            raise forms.ValidationError("Debes seleccionar un tipo de elemento válido.")

        # Seleccionar automáticamente un elemento disponible
        if tipo_elemento == "libro":
            elemento = Libro.objects.filter(prestado=False).first()
        else:
            elemento = JuegoDeMesa.objects.filter(prestado=False).first()

        if not elemento:
            raise forms.ValidationError(
                f"No hay {tipo_elemento}s disponibles para préstamo en este momento."
            )

        # Agregar el elemento al formulario
        cleaned_data["elemento_id"] = elemento.id
        return cleaned_data


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
        fields = ["titulo", "autor"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del libro"}
            ),
            "autor": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Autor"}
            ),
        }
        labels = {
            "titulo": "Nombre del libro",
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
