from django.contrib.auth.models import User
from django.db import models

from product.models import Product, ProductOption


class OrderChoices(models.Choices):
    WAITING = "WAITING"
    PREPARATION = "PREPARATION"
    READY = "READY"
    DELIVER = "DELIVER"


class Order(models.Model):
    status = models.CharField(
        choices=OrderChoices.choices, default=OrderChoices.WAITING, max_length=125
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    options = models.ForeignKey(
        ProductOption, blank=True, null=True, on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
