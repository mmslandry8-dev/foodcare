from django.urls import path

from . import views

urlpatterns = [

    path(
        'process/<int:order_id>/',
        views.process_payment,
        name='process_payment'
    ),

    path(
        'success/<int:pk>/',
        views.payment_success,
        name='payment_success'
    ),

    path(
        'history/',
        views.payment_history,
        name='payment_history'
    ),

    path(
        'invoice/<int:pk>/',
        views.generate_invoice,
        name='generate_invoice'
    ),

]