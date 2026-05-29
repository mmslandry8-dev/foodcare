from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from .models import Reservation

from .forms import ReservationForm


@login_required
def reserve_table(request):
    """
    Réservation table
    """

    if request.method == 'POST':

        form = ReservationForm(request.POST)

        if form.is_valid():

            reservation = form.save(
                commit=False
            )

            reservation.user = request.user

            reservation.save()

            messages.success(

                request,

                'Réservation effectuée.'

            )

            return redirect(
                'reservation_list'
            )

    else:

        form = ReservationForm()

    context = {

        'form': form

    }

    return render(
        request,
        'reservations/reserve_table.html',
        context
    )


@login_required
def reservation_list(request):
    """
    Historique réservations
    """

    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {

        'reservations': reservations

    }

    return render(
        request,
        'reservations/reservation_list.html',
        context
    )


@login_required
def cancel_reservation(request, pk):
    """
    Annuler réservation
    """

    reservation = get_object_or_404(

        Reservation,

        id=pk,

        user=request.user

    )

    if reservation.status == 'pending':

        reservation.status = 'cancelled'

        reservation.save()

        messages.warning(

            request,

            'Réservation annulée.'

        )

    return redirect(
        'reservation_list'
    )


@staff_member_required
def admin_reservations(request):
    """
    Gestion admin réservations
    """

    reservations = Reservation.objects.order_by(
        '-created_at'
    )

    context = {

        'reservations': reservations

    }

    return render(
        request,
        'reservations/admin_reservations.html',
        context
    )