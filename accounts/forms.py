from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):
    """
    Formulaire d'inscription
    """

    first_name = forms.CharField(
        max_length=100
    )

    last_name = forms.CharField(
        max_length=100
    )

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [

            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'

        ]


class ProfileForm(forms.ModelForm):
    """
    Formulaire du profil utilisateur
    """

    class Meta:

        model = Profile

        fields = [

            'phone',
            'address',
            'diabetes_type',
            'image'

        ]