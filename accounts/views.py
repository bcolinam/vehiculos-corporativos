from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User

# --- Formulario de Edición de Perfil ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# --- Formulario de Registro con campos extendidos ---
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

# --- Vistas ---

@user_passes_test(lambda u: u.is_staff)
def signup(request):
    """Permite que un administrador cree nuevos usuarios del sistema."""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"¡Cuenta para {user.username} creada con éxito!")
            return redirect("vehiculos:dashboard")
    else:
        form = SignUpForm()
    
    return render(request, "registration/signup.html", {"form": form})

@login_required
def profile(request):
    """Muestra la información de perfil del usuario logueado."""
    return render(request, "accounts/profile.html", {"user": request.user})

@login_required
def profile_edit(request):
    """Permite al usuario logueado actualizar su propia información básica."""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado correctamente!")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Error al actualizar el perfil. Verifica los datos.")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})