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

@staff_member_required
def update_reservation_status(request, pk):
    """
    Mise à jour statut réservation
    """

    reservation = get_object_or_404(

        Reservation,
        id=pk

    )

    if request.method == 'POST':

        new_status = request.POST.get(
            'status'
        )

        allowed_transitions = {

            'pending': [

                'confirmed',
                'cancelled'

            ],

            'confirmed': [

                'completed'

            ],

            'completed': [],

            'cancelled': [],

        }

        if new_status in allowed_transitions[
            reservation.status
        ]:

            reservation.status = new_status

            reservation.save()

            messages.success(

                request,

                'Réservation mise à jour.'

            )

        else:

            messages.error(

                request,

                'Transition interdite.'

            )

        return redirect(
            'admin_reservations'
        )

    context = {

        'reservation': reservation

    }

    return render(

        request,

        'reservations/update_reservation.html',

        context

    )