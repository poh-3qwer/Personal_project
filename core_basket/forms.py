from django.forms import ModelForm
from core_basket.models import *


class BasketItemEditForm(ModelForm):

    class Meta:
        model = BasketItem
        fields = ['quantity',]