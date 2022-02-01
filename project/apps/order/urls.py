
from django.conf.urls import url
from django.contrib import admin
from project.apps.order.views import CheckoutView, ShippingAddresView, OrderView, BasketView, BasketItemView

from rest_framework.routers import SimpleRouter


router = SimpleRouter()

# Topic Viewset

router.register('shipping-address', ShippingAddresView, basename='shipping-address'),
router.register('order', OrderView, basename='order'),
router.register('basket', BasketView, basename='basket'),
router.register('basket-item', BasketItemView, basename='basket-item'),

urlpatterns = [
    url('checkout/', CheckoutView.as_view(), name="order-checkout"),
]+router.urls
