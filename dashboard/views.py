from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from django.db.models import Sum

from django.contrib.auth.models import User

from meals.models import Meal

from orders.models import Order

from reservations.models import Reservation


@staff_member_required
def dashboard_home(request):
    """
    Dashboard principal
    """

    total_users = User.objects.count()

    total_meals = Meal.objects.count()

    total_orders = Order.objects.count()

    total_reservations = Reservation.objects.count()

    revenue = Order.objects.filter(

        status='delivered'

    ).aggregate(

        Sum('total_price')

    )['total_price__sum'] or 0

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:5]

    context = {

        'total_users': total_users,

        'total_meals': total_meals,

        'total_orders': total_orders,

        'revenue': revenue,

        'recent_orders': recent_orders,

        'total_reservations': total_reservations,

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@staff_member_required
def dashboard_orders(request):
    """
    Gestion commandes
    """

    orders = Order.objects.order_by(
        '-created_at'
    )

    context = {

        'orders': orders

    }

    return render(
        request,
        'dashboard/orders.html',
        context
    )


@staff_member_required
def update_order_status(request, pk):
    """
    Mise à jour statuts
    """

    order = get_object_or_404(
        Order,
        id=pk
    )

    if request.method == 'POST':

        new_status = request.POST.get(
            'status'
        )

        # =========================
        # LOGIQUE IRREVERSIBLE
        # =========================

        allowed_transitions = {

            'pending': ['ready', 'cancelled'],

            'ready': ['delivery'],

            'delivery': ['delivered'],

            'delivered': [],

            'cancelled': [],

        }

        if new_status in allowed_transitions[
            order.status
        ]:

            order.status = new_status

            order.save()

            messages.success(

                request,

                'Statut mis à jour.'

            )

        else:

            messages.error(

                request,

                'Transition interdite.'

            )

        return redirect(
            'dashboard_orders'
        )

    context = {

        'order': order

    }

    return render(
        request,
        'dashboard/order_update.html',
        context
    )