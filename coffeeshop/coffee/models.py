from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from coffee.email import send_mail_order_updated


class ProductOption(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class ProductOptionValue(models.Model):
    option = models.ForeignKey(
        ProductOption, related_name="option_values", on_delete=models.CASCADE
    )
    value = models.CharField(max_length=20)


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="product/", null=True)
    product_option = models.ForeignKey(
        ProductOption, related_name="products", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class ProductOrder(TimeStampedModel):
    WAITING = "waiting"
    PREPARATION = "preparation"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELED = "canceled"

    ORDER_CHOICES = (
        (WAITING, _("Waiting")),
        (PREPARATION, _("Preparation")),
        (READY, _("Ready")),
        (DELIVERED, _("Delivered")),
        (CANCELED, _("Canceled")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_orders", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_orders", on_delete=models.CASCADE
    )
    option_value = models.ForeignKey(
        ProductOptionValue, on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        _("Order Status"), choices=ORDER_CHOICES, default=WAITING, max_length=12
    )


@receiver(pre_save, sender=ProductOrder)
def on_change_status(sender, instance, **kwargs):
    if instance.id is not None:
        previous = sender.objects.get(id=instance.id)
        if previous.status != instance.status:  # field will be updated
            send_mail_order_updated(instance)
