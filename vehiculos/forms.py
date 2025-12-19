from django import forms
from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    """
    Formulario para el registro y edición de vehículos corporativos.

    Responsabilidades:
    - Validar datos de entrada
    - Aplicar reglas de negocio
    - Mejorar la experiencia del usuario
    """

    class Meta:
        model = Vehiculo
        fields = [
            "usuario",
            "patente",
            "marca",
            "modelo",
            "activo",
        ]

        labels = {
            "usuario": "Usuario asignado",
            "patente": "Patente",
            "marca": "Marca",
            "modelo": "Modelo",
            "activo": "Activo",
        }

        widgets = {
            "usuario": forms.Select(attrs={"class": "form-control"}),
            "patente": forms.TextInput(
                attrs={
                    "placeholder": "Ej: AB-CD-12",
                    "class": "form-control",
                }
            ),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(),
        }

    def clean_patente(self):
        """
        Validación de la patente.

        Reglas básicas:
        - Se almacena en mayúsculas
        - Se eliminan espacios laterales
        """
        patente = self.cleaned_data.get("patente", "").strip().upper()

        if len(patente) < 5:
            raise forms.ValidationError(
                "La patente ingresada no es válida."
            )

        return patente
