from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

import meals

from .models import Meal, Category
from .forms import MealForm

from .utils import get_recommended_meals

from django.contrib.admin.views.decorators import staff_member_required


def meal_list(request):
    """
    Liste des repas + recherche + filtres
    """

    meals = Meal.objects.filter(
        is_available=True
    )

    categories = Category.objects.all()

    # =========================
    # RECHERCHE
    # =========================

    query = request.GET.get('q')

    if query:

        meals = meals.filter(

            name__icontains=query

        ) | meals.filter(

            ingredients__icontains=query

        ) | meals.filter(

            category__name__icontains=query

        )

    # =========================
    # FILTRE TYPE DIABETE
    # =========================

    diabetes_type = request.GET.get(
        'diabetes'
    )

    if diabetes_type:

        meals = meals.filter(
            diabetes_type=diabetes_type
        )

    # =========================
    # FILTRES NUTRITIONNELS
    # =========================

    if request.GET.get('low_sugar'):

        meals = meals.filter(
            is_low_sugar=True
        )

    if request.GET.get('low_carb'):

        meals = meals.filter(
            is_low_carb=True
        )

    if request.GET.get('high_fiber'):

        meals = meals.filter(
            is_high_fiber=True
        )

    if request.GET.get('vegetarian'):

        meals = meals.filter(
            is_vegetarian=True
        )

    if request.GET.get('vegan'):

        meals = meals.filter(
            is_vegan=True
        )

    context = {

        'meals': meals,
        'categories': categories

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

    recommended_meals = Meal.objects.filter(

        diabetes_type=meal.diabetes_type,
        is_available=True

    ).exclude(

        id=meal.id

    )[:3]

    context = {

        'meal': meal,
        'recommended_meals': recommended_meals

    }

    return render(
        request,
        'meals/meal_detail.html',
        context
    )


@login_required
@staff_member_required
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

@login_required
def recommendations(request):
    """
    Recommandations nutritionnelles
    """

    diabetes_type = request.GET.get(
        'type',
        'type2'
    )

    meals = get_recommended_meals(
        diabetes_type
    )

    context = {

        'meals': meals,

        'selected_type': diabetes_type

    }

    return render(

        request,

        'meals/recommendations.html',

        context

    )

@login_required
@staff_member_required
def meal_update(request, pk):

    meal = get_object_or_404(
        Meal,
        pk=pk
    )

    form = MealForm(
        request.POST or None,
        request.FILES or None,
        instance=meal
    )

    if form.is_valid():

        form.save()

        return redirect(
            'menu_management'
        )

    return render(
        request,
        'meals/meal_update.html',
        {'form': form}
    )


@login_required
@staff_member_required
def meal_delete(request, pk):

    meal = get_object_or_404(
        Meal,
        pk=pk
    )

    if request.method == 'POST':

        meal.delete()

        return redirect(
            'menu_management'
        )

    return render(
        request,
        'meals/meal_delete.html',
        {'meal': meal}
    )