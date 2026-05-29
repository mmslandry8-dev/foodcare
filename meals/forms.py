from django import forms
from .models import Meal


class MealForm(forms.ModelForm):
    """
    Formulaire des repas
    """

    class Meta:

        model = Meal

        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                'class': 'form-control'

            })