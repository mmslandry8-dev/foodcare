from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from django.db.models import Sum

from django.contrib.auth.models import User

from meals.models import Meal

from orders.models import Order

from reservations.models import Reservation

from payments.models import Payment

from reportlab.pdfgen import canvas
from django.http import HttpResponse

@staff_member_required
def dashboard_home(request):
    """
    Dashboard principal
    """

    total_users = User.objects.count()

    total_meals = Meal.objects.count()

    total_orders = Order.objects.count()

    total_reservations = Reservation.objects.count()

    total_payments = Payment.objects.count()

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

        'total_payments': total_payments,

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

@staff_member_required
def menu_management(request):

    meals = Meal.objects.all().order_by('-id')

    query = request.GET.get('q')

    if query:

        meals = meals.filter(
            name__icontains=query
        )

    context = {
        'meals': meals
    }

    return render(
        request,
        'dashboard/menu_management.html',
        context
    )

@staff_member_required
def admin_payments(request):

    payments = Payment.objects.all().order_by('-id')

    context = {

        'payments': payments

    }

    return render(
        request,
        'dashboard/admin_payments.html',
        context
    )

@staff_member_required
def admin_invoice(request, pk):

    payment = get_object_or_404(
        Payment,
        id=pk
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="facture_{payment.id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(200, 800, "FACTURE FOODCARE")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        740,
        f"Client : {payment.order.user.username}"
    )

    pdf.drawString(
        50,
        720,
        f"Commande : #{payment.order.id}"
    )

    pdf.drawString(
        50,
        700,
        f"Transaction : {payment.transaction_id}"
    )

    pdf.drawString(
        50,
        680,
        f"Montant : {payment.amount} FCFA"
    )

    pdf.drawString(
        50,
        660,
        f"Méthode : {payment.get_method_display()}"
    )

    pdf.drawString(
        50,
        640,
        f"Statut : {payment.get_status_display()}"
    )

    y = 580

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Produits commandés"
    )

    y -= 40

    pdf.setFont(
        "Helvetica",
        12
    )

    for item in payment.order.items.all():

        pdf.drawString(
            50,
            y,
            f"{item.meal.name} x{item.quantity}"
        )

        pdf.drawString(
            400,
            y,
            f"{item.total_price} FCFA"
        )

        y -= 25

    pdf.drawString(
        50,
        100,
        "Merci de votre confiance."
    )

    pdf.save()

    return response