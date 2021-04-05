from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = "order"

    def ready(self):
        from . import signal

        super(OrderConfig, self).ready()
