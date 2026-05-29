from django.db import models
from django.contrib.auth.models import User

from meals.models import Meal


class Order(models.Model):
    """
    Commande utilisateur
    """

    STATUS_CHOICES = [

        ('pending', 'En attente'),

        ('ready', 'Prête'),

        ('delivery', 'En livraison'),

        ('delivered', 'Livrée'),

        ('cancelled', 'Annulée'),

    ]

    PAYMENT_CHOICES = [

        ('mobile_money', 'Mobile Money'),

        ('card', 'Carte bancaire'),

        ('cash', 'Paiement livraison'),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    delivery_address = models.TextField()

    def __str__(self):

        return f"Commande #{self.id}"

    @property
    def can_confirm_delivery(self):
        """
        Affiche le bouton 'J'ai reçu'
        """

        return self.status == 'delivery'


class OrderItem(models.Model):
    """
    Détails commande
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return self.meal.name

    @property
    def total_price(self):

        return self.quantity * self.price