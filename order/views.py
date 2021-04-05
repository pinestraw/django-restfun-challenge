from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from order.serializers import OrderReadSerializer, OrderWriteSerializer

from .models import Order
from .permissions import OrderPermission


class OrderViewSet(ModelViewSet):
    serializer_class = OrderReadSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (OrderPermission,)
    queryset = Order.objects.all().order_by("-id")

    def get_queryset(self):
        qs = super(OrderViewSet, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderWriteSerializer
        return super(OrderViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
