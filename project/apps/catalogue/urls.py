from .views import ProductViewset
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()

router.register('products', ProductViewset, basename='products')

urlpatterns = router.urls