from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Suppression des help_text
        for field in self.fields.values():

            field.help_text = ''

            field.widget.attrs.update({

                'class': 'form-control'

            })

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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                'class': 'form-control'

            })

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