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

    recommended_for = models.CharField(
        max_length=20,
        choices=DIABETES_CHOICES,
        default='type2'
    )

    fiber = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    sugar = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
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

    is_gluten_free = models.BooleanField(
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

    @property
    def health_score(self):
        """
        Calcul intelligent score santé
        """

        score = 100

        # Pénalités glucides
        if self.carbohydrates > 50:
            score -= 20

        elif self.carbohydrates > 30:
            score -= 10

        # Pénalités calories
        if self.calories > 800:
            score -= 15

        # Bonus fibres
        if self.fiber > 10:
            score += 10

        # Bonus faible sucre
        if self.sugar < 10:
            score += 5

        # Bonus faible IG
        if self.glycemic_index < 55:
            score += 10

        return max(score, 0)

    @property
    def nutrition_badges(self):

        badges = []

        if self.is_low_carb:
            badges.append("Faible glucides")

        if self.is_gluten_free:
            badges.append("Sans gluten")

        if self.is_vegan:
            badges.append("Vegan")

        if self.glycemic_index < 55:
            badges.append("IG faible")

        if self.is_high_fiber:
            badges.append("Riche fibres")

        return badges