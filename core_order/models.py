from django.db import models
from core_profile.models import Account
from core_menu.models import Instrument


class Order(models.Model):

    PAYMENT_CHOICES = [
                       ('cash_when_delivered', 'Готівка при отриманні'),
                       ('online_payment', 'Онлайн оплата'),
                    ]

    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлений'),
        ('completed', 'Виконаний'),
        ('cancelled', 'Скасований'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account')
    payment = models.CharField(max_length=45, choices=PAYMENT_CHOICES, default='cash_when_delivered')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    delivery_adress = models.TextField()
    total_price = models.IntegerField(default=0)
    date_of_creation = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveBigIntegerField()
    instrument= models.ForeignKey(Instrument, on_delete=models.PROTECT)
    price = models.IntegerField()
    is_shipped = models.BooleanField(default=False)