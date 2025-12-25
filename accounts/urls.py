from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # --- Autenticación Estándar ---
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/", 
        # Agregamos next_page para redirigir siempre al login tras salir
        auth_views.LogoutView.as_view(next_page="accounts:login"), 
        name="logout"
    ),

    # --- Gestión de Usuario y Perfil ---
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),

    # --- Gestión de Seguridad (Cambio de Contraseña) ---
    path(
        "password-change/", 
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            # Aseguramos que redirija al 'done' de este mismo namespace
            success_url="/accounts/password-change/done/"
        ),
        name="password_change"
    ),
    path(
        "password-change/done/", 
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done"
    ),
]