from django.db import models
from core_menu.models import Instrument
from core_profile.models import Account


class Basket(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='basket')

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='basket_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['basket', 'product'],
                name='unique_instrument_in_basket'
            )
        ]