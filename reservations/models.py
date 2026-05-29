from django.db import models

from django.contrib.auth.models import User


class Reservation(models.Model):

    STATUS_CHOICES = [

        ('pending', 'En attente'),

        ('confirmed', 'Confirmée'),

        ('cancelled', 'Annulée'),

        ('completed', 'Terminée'),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reservation_date = models.DateField()

    reservation_time = models.TimeField()

    number_of_guests = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    special_request = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return f"Réservation #{self.id}"

    @property
    def is_past(self):

        from django.utils.timezone import now

        return self.reservation_date < now().date()