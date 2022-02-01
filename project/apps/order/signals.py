
from django.db.models.signals import post_save
from django.dispatch import receiver
from project.apps.order import utils


def some_function(sender, instance, created, **kwargs):
    utils.order_notification_to_user()
    utils.process_order()
