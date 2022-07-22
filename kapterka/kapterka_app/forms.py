from django import forms

from .models import Equipment


class AddEquipmentForm(forms.ModelForm):

    name = forms.CharField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

        # TODO self.fields['type_of_hike'] = "Вид туризма не выбран"

        # class Meta:
        #     model = Equipment
        #     fields = ['name', 'type_of_hike', 'unique', 'number', 'price', 'price_per_day', 'price_for_members',
        #               'description']
