from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Catégorie des repas
    """

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    def __str__(self):

        return self.name


class Meal(models.Model):
    """
    Modèle des repas FoodCare
    """

    DIABETES_CHOICES = [

        ('type1', 'Diabète Type 1'),
        ('type2', 'Diabète Type 2'),
        ('prediabetes', 'Prédiabète'),

    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='meals'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    ingredients = models.TextField()

    image = models.ImageField(
        upload_to='meals/'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    calories = models.PositiveIntegerField()

    carbohydrates = models.PositiveIntegerField()

    proteins = models.PositiveIntegerField()

    lipids = models.PositiveIntegerField()

    glycemic_index = models.PositiveIntegerField()

    allergens = models.TextField(
        blank=True
    )

    diabetes_type = models.CharField(
        max_length=20,
        choices=DIABETES_CHOICES
    )

    is_available = models.BooleanField(
        default=True
    )

    is_low_sugar = models.BooleanField(
        default=False
    )

    is_low_carb = models.BooleanField(
        default=False
    )

    is_high_fiber = models.BooleanField(
        default=False
    )

    is_vegetarian = models.BooleanField(
        default=False
    )

    is_vegan = models.BooleanField(
        default=False
    )

    is_popular = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name

    def get_absolute_url(self):

        return reverse(
            'meal_detail',
            kwargs={'pk': self.pk}
        )