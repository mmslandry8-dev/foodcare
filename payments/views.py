import uuid

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Payment

from orders.models import Order

from django.http import HttpResponse

from reportlab.pdfgen import canvas

@login_required
def process_payment(request, order_id):
    """
    Simulation paiement
    """

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user

    )

    # Vérifie si paiement existe déjà
    existing_payment = Payment.objects.filter(
        order=order
    ).first()

    if existing_payment:

        messages.info(

            request,

            'Paiement déjà effectué.'

        )

        return redirect(
            'payment_history'
        )

    # =========================
    # CREATION PAIEMENT
    # =========================

    payment = Payment.objects.create(

        order=order,

        amount=order.total_price,

        method=order.payment_method,

        status='validated',

        transaction_id=str(uuid.uuid4())[:12]

    )

    messages.success(

        request,

        'Paiement effectué avec succès.'

    )

    return redirect(
        'payment_success',
        payment.id
    )


@login_required
def payment_success(request, pk):
    """
    Succès paiement
    """

    payment = get_object_or_404(

        Payment,

        id=pk,

        order__user=request.user

    )

    context = {

        'payment': payment

    }

    return render(

        request,

        'payments/payment_success.html',

        context

    )


@login_required
def payment_history(request):
    """
    Historique paiements
    """

    payments = Payment.objects.filter(

        order__user=request.user

    ).order_by('-created_at')

    context = {

        'payments': payments

    }

    return render(

        request,

        'payments/payment_history.html',

        context

    )

@login_required
def generate_invoice(request, pk):
    """
    Génération facture PDF
    """

    payment = get_object_or_404(

        Payment,

        id=pk,

        order__user=request.user

    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (

        f'attachment; filename="facture_{payment.id}.pdf"'

    )

    pdf = canvas.Canvas(response)

    # =========================
    # HEADER
    # =========================

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        200,
        800,
        "FACTURE FOODCARE"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    # =========================
    # INFOS CLIENT
    # =========================

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
        f"Paiement : {payment.get_method_display()}"
    )

    pdf.drawString(
        50,
        640,
        f"Statut : {payment.get_status_display()}"
    )

    # =========================
    # PRODUITS
    # =========================

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

    # =========================
    # FOOTER
    # =========================

    pdf.drawString(
        50,
        100,
        "Merci de votre confiance."
    )

    pdf.save()

    return response