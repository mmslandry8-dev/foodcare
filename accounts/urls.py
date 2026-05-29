from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    # Inscription
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # Connexion
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    # Déconnexion
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Profil
    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

]