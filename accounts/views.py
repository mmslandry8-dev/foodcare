from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ProfileForm
from .models import Profile


def register_view(request):
    """
    Vue d'inscription utilisateur
    """

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            # Création utilisateur
            user = form.save()

            # Création profil associé
            Profile.objects.create(
                user=user
            )

            # Connexion automatique
            login(request, user)

            messages.success(
                request,
                'Compte créé avec succès.'
            )

            return redirect('home')

    else:

        form = RegisterForm()

    context = {

        'form': form

    }

    return render(
        request,
        'accounts/register.html',
        context
    )


def logout_view(request):
    """
    Déconnexion utilisateur
    """

    logout(request)

    messages.warning(
        request,
        'Vous êtes déconnecté.'
    )

    return redirect('home')


@login_required
def profile_view(request):
    """
    Gestion du profil utilisateur
    """

    profile = request.user.profile

    if request.method == 'POST':

        form = ProfileForm(

            request.POST,
            request.FILES,
            instance=profile

        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profil mis à jour.'
            )

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    context = {

        'form': form

    }

    return render(
        request,
        'accounts/profile.html',
        context
    )