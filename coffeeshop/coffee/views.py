from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from coffee.models import Product, ProductOrder
from coffee.serializers import ProductSerializer, ProductOrderSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductOrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductOrderSerializer

    def get_queryset(self):
        return ProductOrder.objects.filter(user=self.request.user)
