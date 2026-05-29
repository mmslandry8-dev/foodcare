from .models import Meal


def get_recommended_meals(diabetes_type):
    """
    Recommandations intelligentes
    """

    meals = Meal.objects.filter(
        recommended_for=diabetes_type,
        is_available=True
    )

    if diabetes_type == 'type1':

        meals = meals.order_by(
            '-fiber',
            'carbohydrates'
        )

    elif diabetes_type == 'type2':

        meals = meals.order_by(
            'carbohydrates',
            'glycemic_index'
        )

    elif diabetes_type == 'prediabetes':

        meals = meals.order_by(
            'glycemic_index',
            '-fiber'
        )

    return meals