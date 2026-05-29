from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'user',
        'reservation_date',
        'reservation_time',
        'number_of_guests',
        'status',

    )

    list_filter = (

        'status',
        'reservation_date',

    )

    search_fields = (

        'user__username',

    )