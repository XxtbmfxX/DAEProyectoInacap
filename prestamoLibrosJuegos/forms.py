from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            "alumno",
            "fecha_inicio",
            "fecha_termino",
            "content_type",
            "object_id",
        ]

        widgets = {
            "alumno": forms.Select(
                attrs={
                    "class": "form-select",  # Estilo de Bootstrap
                }
            ),
            "fecha_inicio": forms.DateInput(
                format="%d/%m/%Y",
                attrs={
                    "class": "form-control",
                    "placeholder": "DD/MM/YYYY",
                    "type": "date",
                },
            ),
            "fecha_termino": forms.DateInput(
                format="%d/%m/%Y",
                attrs={
                    "class": "form-control",
                    "placeholder": "DD/MM/YYYY",
                    "type": "date",
                },
            ),
            "content_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "object_id": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ID del elemento (Libro o Juego)",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_termino = cleaned_data.get("fecha_termino")

        # Validación de rango de fechas
        if fecha_inicio and fecha_termino and fecha_termino < fecha_inicio:
            raise forms.ValidationError(
                "La fecha de término no puede ser anterior a la de inicio."
            )
        return cleaned_data
