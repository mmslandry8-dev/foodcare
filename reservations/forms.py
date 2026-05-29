from django import forms

from django.utils.timezone import now

from .models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:

        model = Reservation

        fields = [

            'reservation_date',
            'reservation_time',
            'number_of_guests',
            'special_request',

        ]

        widgets = {

            'reservation_date': forms.DateInput(

                attrs={

                    'type': 'date',

                    'class': 'form-control'

                }

            ),

            'reservation_time': forms.TimeInput(

                attrs={

                    'type': 'time',

                    'class': 'form-control'

                }

            ),

            'number_of_guests': forms.NumberInput(

                attrs={

                    'class': 'form-control',

                    'min': 1,

                    'max': 20

                }

            ),

            'special_request': forms.Textarea(

                attrs={

                    'class': 'form-control',

                    'rows': 4,

                    'placeholder': 'Demandes spéciales...'

                }

            ),

        }

    # =========================
    # VALIDATION DATE
    # =========================

    def clean_reservation_date(self):

        reservation_date = self.cleaned_data[
            'reservation_date'
        ]

        if reservation_date < now().date():

            raise forms.ValidationError(

                "Impossible de réserver dans le passé."

            )

        return reservation_date

    # =========================
    # VALIDATION HEURE
    # =========================

    def clean_reservation_time(self):

        reservation_time = self.cleaned_data[
            'reservation_time'
        ]

        opening_time = "08:00"

        closing_time = "22:00"

        time_string = reservation_time.strftime(
            '%H:%M'
        )

        if time_string < opening_time:

            raise forms.ValidationError(

                "Le restaurant ouvre à 08h00."

            )

        if time_string > closing_time:

            raise forms.ValidationError(

                "Le restaurant ferme à 22h00."

            )

        return reservation_time

    # =========================
    # VALIDATION GLOBALE
    # =========================

    def clean(self):

        cleaned_data = super().clean()

        reservation_date = cleaned_data.get(
            'reservation_date'
        )

        reservation_time = cleaned_data.get(
            'reservation_time'
        )

        guests = cleaned_data.get(
            'number_of_guests'
        )

        if reservation_date and reservation_time:

            # =========================
            # CAPACITE MAXIMALE
            # =========================

            existing_reservations = Reservation.objects.filter(

                reservation_date=reservation_date,

                reservation_time=reservation_time,

                status__in=[

                    'pending',
                    'confirmed'

                ]

            )

            total_reserved = sum(

                reservation.number_of_guests

                for reservation in existing_reservations

            )

            restaurant_capacity = 40

            if total_reserved + guests > restaurant_capacity:

                raise forms.ValidationError(

                    "Capacité maximale du restaurant atteinte."

                )

        return cleaned_data