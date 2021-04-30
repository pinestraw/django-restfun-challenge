from django.db import models
from django.contrib.auth.models import User
from product.models import *
from restfun.helpers import send_email
from django.core.exceptions import ObjectDoesNotExist

class StatusOrder(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return 'Status of the order: %s' % ( self.description )

class Order(models.Model):
    status = models.ForeignKey(
        StatusOrder, 
        on_delete=models.PROTECT
        )
    user   = models.ForeignKey(
        User,
        on_delete=models.PROTECT
        )
    consume_location = models.CharField(
        max_length=1,
        choices=[('T', 'Take away'),('I', 'In shop')],
        default='I'
        )

    @classmethod
    def get_current(cls, user):
        try:
            order = cls.objects.get(user=user, status=StatusOrder.objects.get(description='Waiting'))
        except ObjectDoesNotExist:
            order = cls()
        return order

    def __str__(self):
        return 'Order number: %i, created by %s to %s' % ( self.pk , self.user.email, self.consume_location )

    def save(self, *args, **kwargs):
        """Override the save method of object order to send e-mail on any change of status"""
        if self._state.adding is False:
            order_ = Order.objects.get(pk=self.pk)
            try:
                super().save(*args, **kwargs)
                if (order_.status != self.status) and (self.user.email is not None):
                    send_email([self.user.email],
                    'Status changed',
                    'The order: %i status changed to: %s' % (self.pk, self.status.description))
            except:
                pass
        else:
            super().save(*args, **kwargs)

    def price(self):
        if self._state.adding is False:
            order_item_ = OrderItem.objects.filter(order=self)
            price_      = 0.
            for item in order_item_:
                price_ += item.price()
            return price_
        return 0.0

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute = models.ForeignKey(OptionAttributeProduct, on_delete=models.PROTECT, null=True, blank=True)
    quantity  = models.IntegerField(default=1)
    def __str__(self):
        return 'Order number %i - %s' % ( self.order.pk, self.product )

    def price(self):
        price_ = self.attribute.price_perc if self.attribute else 1.0
        return self.product.price * price_ * self.quantity
