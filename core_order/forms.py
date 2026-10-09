from django import forms
from core_order.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['delivery_adress', 'payment']

        widgets = {
            'delivery_adress': forms.Textarea(attrs={
                'placeholder': 'Введіть адресу доставки',
                'rows': 3,
            }),
            'payment': forms.Select(),
        }