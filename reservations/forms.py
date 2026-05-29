from django import forms

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