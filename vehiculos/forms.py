from django import forms
from .models import Vehiculo
from django.contrib.auth.models import User
import re

class VehiculoForm(forms.ModelForm):
    """
    Formulario optimizado para la gestión de flota corporativa.
    Incluye validación avanzada de patentes y personalización de selección de usuarios.
    """

    # Personalizamos el queryset del usuario para que se vea Nombre + Apellido
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Usuario Responsable",
        empty_label="--- Sin asignar (Flota en reserva) ---",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Vehiculo
        fields = ["usuario", "patente", "marca", "modelo", "anio", "color", "activo"]
        
        widgets = {
            "patente": forms.TextInput(attrs={"placeholder": "AAAA11 o AA1122", "class": "form-control"}),
            "marca": forms.TextInput(attrs={"placeholder": "Ej: Toyota", "class": "form-control"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ej: Hilux", "class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"placeholder": "Ej: Blanco", "class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modificamos la representación del usuario en el desplegable
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.username})" if obj.get_full_name() else obj.username

    def clean_patente(self):
        """
        Limpia y valida la patente chilena.
        Elimina guiones, espacios y verifica formato alfanumérico.
        """
        patente = self.cleaned_data.get("patente", "").strip().upper()
        # Eliminar cualquier caracter no alfanumérico (guiones, espacios, puntos)
        patente = re.sub(r'[^A-Z0-9]', '', patente)

        # Validación de longitud (Estándar chileno actual es de 6 caracteres)
        if len(patente) < 5 or len(patente) > 6:
            raise forms.ValidationError(
                "La patente debe tener entre 5 y 6 caracteres alfanuméricos."
            )
        
        # Opcional: Validar que el vehículo no esté ya registrado con esa patente corregida
        # (Django ya lo hace por el 'unique=True' en el modelo, pero aquí podemos personalizar el error)
        return patente

    def clean_anio(self):
        anio = self.cleaned_data.get("anio")
        import datetime
        current_year = datetime.date.today().year
        if anio and (anio < 1980 or anio > current_year + 1):
            raise forms.ValidationError(f"El año debe estar entre 1980 y {current_year + 1}")
        return anio