from django.db import models
from django.conf import settings


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    market_volume = models.CharField(max_length=100)
    change = models.CharField(max_length=100)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

