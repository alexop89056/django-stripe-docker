import secrets

from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('rub', 'Рубли'),
        ('usd', 'Доллары')
    ]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES, default='rub')

    def __str__(self):
        return f'<Item {self.id}, Name: {self.name}>'


def get_order_id():
    return secrets.token_urlsafe(64)


class Order(models.Model):
    order_id = models.TextField(default=get_order_id)
    total_price = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)