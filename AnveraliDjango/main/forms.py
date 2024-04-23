from django import forms
from .models import Orders


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['title', 'description', 'price']
        labels = {
            'title': 'Название ',
            'description': 'Описание',
            'price': 'Стоимость',
        }
