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

    path(
        'menus/',
        views.menu_management,
        name='menu_management'
    ),

    path(
        'payments/',
        views.admin_payments,
        name='admin_payments'
    ),

    path(
        'payments/invoice/<int:pk>/',
        views.admin_invoice,
        name='admin_invoice'
    ),

]