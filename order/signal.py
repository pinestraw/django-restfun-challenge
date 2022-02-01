import os

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def save_profile(sender, instance, created, raw, using, update_fields, **kwargs):
    if (instance.status != Order.objects.get(id=instance.id).status) or created:
        send_mail(
            "Order Status Changed",
            f"Order status is {instance.status}",
            os.environ.get("EMAIL_HOST_USER"),
            [
                instance.user.email,
            ],
            fail_silently=False,
        )
