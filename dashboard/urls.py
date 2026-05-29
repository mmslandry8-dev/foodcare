from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.dashboard_home,
        name='dashboard'
    ),

    path(
        'orders/',
        views.dashboard_orders,
        name='dashboard_orders'
    ),

    path(
        'orders/<int:pk>/update/',
        views.update_order_status,
        name='update_order_status'
    ),

]