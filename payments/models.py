from django.db import models

from orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = [

        ('pending', 'En attente'),

        ('validated', 'Validé'),

        ('failed', 'Échoué'),

        ('refunded', 'Remboursé'),

    ]

    METHOD_CHOICES = [

        ('mobile_money', 'Mobile Money'),

        ('card', 'Carte bancaire'),

        ('cash', 'Paiement livraison'),

    ]

    order = models.OneToOneField(

        Order,

        on_delete=models.CASCADE

    )

    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    method = models.CharField(

        max_length=20,

        choices=METHOD_CHOICES

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='pending'

    )

    transaction_id = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"Paiement #{self.id}"