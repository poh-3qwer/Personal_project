from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core_profile.models import Account


class Instrument(models.Model):

    CATEGORY_CHOICES = [
        ('string_instruments', 'Струнні'),
        ('wind_instruments', 'Духові'),
        ('percussion_instruments', 'Ударні'),
        ('keyboards', 'Клавішні'),
        ('electromusical', 'Електромузичні'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='string_instruments')
    name = models.CharField(max_length=100, blank=True)
    production_year = models.IntegerField(validators=[MinValueValidator(1900)])
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    product_condition = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    complectation = models.TextField()
    instrument_image = models.ImageField(upload_to='instruments_images/')
    price = models.IntegerField()
    issue_date = models.DateTimeField(auto_now_add=True)
    salesman = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='salesman')