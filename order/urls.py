from rest_framework import routers

from .views import OrderViewSet

router = routers.SimpleRouter()
router.register(r"", OrderViewSet, basename="order")

app_name = "order"
urlpatterns = [] + router.urls
