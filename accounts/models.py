from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Modèle représentant le profil utilisateur
    """

    DIABETES_CHOICES = [

        ('type1', 'Diabète Type 1'),
        ('type2', 'Diabète Type 2'),
        ('prediabetes', 'Prédiabète'),

    ]

    # Relation avec l'utilisateur Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Informations supplémentaires
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    diabetes_type = models.CharField(
        max_length=20,
        choices=DIABETES_CHOICES,
        blank=True
    )

    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username