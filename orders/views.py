from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Order, OrderItem

from meals.models import Meal


@login_required
def cart_view(request):
    """
    Affichage panier
    """

    cart = request.session.get(
        'cart',
        {}
    )

    cart_items = []

    total = 0

    for meal_id, quantity in cart.items():

        meal = Meal.objects.get(
            id=meal_id
        )

        subtotal = meal.price * quantity

        total += subtotal

        cart_items.append({

            'meal': meal,
            'quantity': quantity,
            'subtotal': subtotal

        })

    context = {

        'cart_items': cart_items,
        'total': total

    }

    return render(
        request,
        'orders/cart.html',
        context
    )


@login_required
def add_to_cart(request, meal_id):
    """
    Ajouter au panier
    """

    cart = request.session.get(
        'cart',
        {}
    )

    if str(meal_id) in cart:

        cart[str(meal_id)] += 1

    else:

        cart[str(meal_id)] = 1

    request.session['cart'] = cart

    messages.success(
        request,
        'Repas ajouté au panier.'
    )

    return redirect('meal_list')


@login_required
def remove_from_cart(request, meal_id):
    """
    Supprimer du panier
    """

    cart = request.session.get(
        'cart',
        {}
    )

    if str(meal_id) in cart:

        del cart[str(meal_id)]

    request.session['cart'] = cart

    messages.warning(
        request,
        'Repas supprimé.'
    )

    return redirect('cart')

@login_required
def checkout_view(request):
    """
    Validation commande
    """

    cart = request.session.get(
        'cart',
        {}
    )

    if not cart:

        messages.warning(
            request,
            'Votre panier est vide.'
        )

        return redirect('meal_list')

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method'
        )

        profile = request.user.profile

        # Création commande
        order = Order.objects.create(

            user=request.user,

            payment_method=payment_method,

            delivery_address=profile.address

        )

        total = 0

        # Création détails
        for meal_id, quantity in cart.items():

            meal = Meal.objects.get(
                id=meal_id
            )

            subtotal = meal.price * quantity

            total += subtotal

            OrderItem.objects.create(

                order=order,

                meal=meal,

                quantity=quantity,

                price=meal.price

            )

        # Total commande
        order.total_price = total

        order.save()

        # Vider panier
        request.session['cart'] = {}

        messages.success(
            request,
            'Commande validée.'
        )

        return redirect(
            'process_payment',
            order.id
        )

    return render(
        request,
        'orders/checkout.html'
    )

@login_required
def order_list(request):
    """
    Historique commandes
    """

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {

        'orders': orders

    }

    return render(
        request,
        'orders/order_list.html',
        context
    )


@login_required
def order_detail(request, pk):
    """
    Détails commande
    """

    order = get_object_or_404(

        Order,
        id=pk,
        user=request.user

    )

    context = {

        'order': order

    }

    return render(
        request,
        'orders/order_detail.html',
        context
    )

@login_required
def confirm_delivery(request, pk):
    """
    Confirmation livraison
    """

    order = get_object_or_404(

        Order,
        id=pk,
        user=request.user

    )

    if order.status == 'delivery':

        order.status = 'delivered'

        order.save()

        messages.success(
            request,
            'Commande livrée.'
        )

    return redirect(
        'order_detail',
        order.id
    )