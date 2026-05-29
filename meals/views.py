from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from .models import Meal
from .forms import MealForm


def meal_list(request):
    """
    Liste des repas
    """

    meals = Meal.objects.filter(
        is_available=True
    )

    context = {

        'meals': meals

    }

    return render(
        request,
        'meals/meal_list.html',
        context
    )


def meal_detail(request, pk):
    """
    Détails d'un repas
    """

    meal = get_object_or_404(
        Meal,
        pk=pk
    )

    context = {

        'meal': meal

    }

    return render(
        request,
        'meals/meal_detail.html',
        context
    )


@login_required
def meal_create(request):
    """
    Création d'un repas
    """

    form = MealForm(

        request.POST or None,
        request.FILES or None

    )

    if form.is_valid():

        form.save()

        return redirect('meal_list')

    context = {

        'form': form

    }

    return render(
        request,
        'meals/meal_create.html',
        context
    )