from django.urls import path

from . import views

urlpatterns = [

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    path(
        'add/<int:meal_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'remove/<int:meal_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        views.checkout_view,
        name='checkout'
    ),

    path(
        'my-orders/',
        views.order_list,
        name='order_list'
    ),

    path(
        '<int:pk>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        'confirm-delivery/<int:pk>/',
        views.confirm_delivery,
        name='confirm_delivery'
    ),

]