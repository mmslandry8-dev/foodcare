from django.urls import path
from . import views

urlpatterns = [

    # Page d'accueil
    path('', views.home, name='home'),

]