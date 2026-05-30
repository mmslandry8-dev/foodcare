from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.meal_list,
        name='meal_list'
    ),

    path(
        '<int:pk>/',
        views.meal_detail,
        name='meal_detail'
    ),

    path(
        'create/',
        views.meal_create,
        name='meal_create'
    ),

    path(
        'recommendations/',
        views.recommendations,
        name='recommendations'
    ),

    path(
        'edit/<int:pk>/',
        views.meal_update,
        name='meal_update'
    ),

    path(
        'delete/<int:pk>/',
        views.meal_delete,
        name='meal_delete'
    ),

    

]