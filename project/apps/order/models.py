
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from project.apps.order.signals import some_function
from django.db.models import signals
from project.apps.catalogue.models import Product
from django.utils.translation import gettext_lazy as _
import jsonfield

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (MERGED, _("Merged - superceded by another basket")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)
    basket_total = models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_basket_total(self):
        basket_total = 0
        for item in BasketItem.objects.filter(basket__id=self.id):
            basket_total+=item.item.selling_price * item.quantity
        return basket_total


    def is_backet_open(self):
        return self.status == Basket.OPEN

    def save(self, *args, **kwargs):
        self.basket_total = self.get_basket_total()
        return super(Basket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.id)


class BasketItem(models.Model):
    basket = models.ForeignKey('Basket',on_delete=models.CASCADE,related_name='lines',verbose_name=_("Basket"))
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def is_item_available(self):
        return self.item.is_available

    def validate_stocks(self):
        return self.quantity <= self.item.stock

    def validate_basket_status(self):
        return self.basket.status == Basket.OPEN


    def is_exists(self):
        return BasketItem.objects.filter(
                basket = self.basket, item = self.item
            ).exclude(id=self.id).exists()


    def clean(self):
        #validate at veiw level
        if not self.validate_basket_status():
            raise ValidationError('Basket status should be open in order to add the item')
        #validate at veiw level
        if self.is_exists():
            raise ValidationError('Requested item already exists in the basket, please update the quantity in previosuly added product')
        #validate at veiw level
        if not self.is_item_available():
            raise ValidationError('Requested item is out of stock')

        if not self.validate_stocks():
            raise ValidationError('Available stocks is lower then requested stocks, available stocks for the item {}'.format(self.item.stock))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BasketItem, self).save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    order_number = models.CharField(max_length=20,blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    basket = models.ForeignKey('Basket',on_delete=models.CASCADE,related_name="backet",verbose_name=_("Cart"))
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = jsonfield.JSONField(default=dict)
    coupon = jsonfield.JSONField(default=dict)

    WAITING, PROCESS, DELIVERED, CANCEL, READY = (
        "Waiting", "Preparation", "Delivered", "Cancel", "Ready")
    STATUS_CHOICES = (
        (WAITING, _("WAITING - currently active")),
        (PROCESS, _("Preparation - superceded by another basket")),
        (DELIVERED, _("Delivered - for items to be purchased later")),
        (CANCEL, _("Cancel - the basket cannot be modified")),
        (READY, _("Ready")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=WAITING, choices=STATUS_CHOICES)
    order_total = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def generate_order_number(self):
        return 100000 + self.basket.id

    def is_lonely_basket(self):
        return Order.objects.filter(basket=self.basket).exists()

    # def clean(self):
    #     #validate at veiw level
    #     # if not self.basket.is_backet_open():
    #     #     raise ValidationError('Basket status should be open in order to produced the order')

    #     if self.is_lonely_basket():
    #         raise ValidationError('Basket already connected to other order')

    def save(self, *args, **kwargs):
        self.full_clean()
        self.order_total = self.basket.basket_total
        self.order_number = self.generate_order_number()

        self.basket.status = Basket.SUBMITTED
        self.basket.save()


        return super(Order, self).save(*args, **kwargs)


    def __str__(self):
        return "{}  - {} - Value: {}".format(self.order_number, self.status, self.order_total)

signals.post_save.connect(receiver=some_function, sender=Order)
