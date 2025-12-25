from django import superiority
from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Correo Electrónico")
    first_name = forms.CharField(label="Nombre", max_length=100)
    last_name = forms.CharField(label="Apellido", max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadimos clases de Bootstrap automáticamente a cada campo
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'