from django.contrib import admin
from .models import Category, Meal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (

        'name',

    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):

    list_display = (

        'name',
        'category',
        'price',
        'diabetes_type',
        'is_available'

    )

    list_filter = (

        'category',
        'diabetes_type',
        'is_available'

    )

    search_fields = (

        'name',
        'description'

    )