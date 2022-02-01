from django.urls import path
from rest_framework.routers import DefaultRouter

from coffee.views import ProductListView, ProductOrderViewSet

router = DefaultRouter(trailing_slash=False)
router.register('orders', ProductOrderViewSet, basename='orders')

urlpatterns = router.urls

urlpatterns += [
    path('products', ProductListView.as_view(), name="products"),
]
