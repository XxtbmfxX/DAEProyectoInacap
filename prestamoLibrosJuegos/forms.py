from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "telefono", "fecha_ingreso"]
        widgets = {
            "fecha_ingreso": forms.DateInput(
                format="%d/%m/%Y",
                attrs={
                    "class": "form-control",
                    "type": "date",  # Esto genera un calendario en navegadores modernos
                },
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]
        if len(telefono) < 7:
            raise forms.ValidationError("El teléfono debe tener al menos 7 caracteres.")
        return telefono
