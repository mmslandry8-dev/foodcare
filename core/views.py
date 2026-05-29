from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def home(request):
    """
    Vue de la page d'accueil FoodCare
    """

    return render(request, 'core/home.html')