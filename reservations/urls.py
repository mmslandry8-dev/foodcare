from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.reserve_table,
        name='reserve_table'
    ),

    path(
        'my-reservations/',
        views.reservation_list,
        name='reservation_list'
    ),

    path(
        'cancel/<int:pk>/',
        views.cancel_reservation,
        name='cancel_reservation'
    ),

    path(
        'admin-reservations/',
        views.admin_reservations,
        name='admin_reservations'
    ),

]