
# Create your views here.
from rest_framework import status
from project.apps.order import utils
from project.apps.order.models import Basket, Order, Address, Basket, BasketItem
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import views
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from project.apps.order.serializer import CheckoutSerializer, BasketSerializer, ShippingAddressSerializer, BasketItemSerializer
from project.apps.order.utils import notify_user
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class ShippingAddresView(viewsets.ModelViewSet):

    serializer_class = ShippingAddressSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Address.objects.all()
    http_method_names = ["post","get"]

class CheckoutView(CreateAPIView):

    serializer_class = CheckoutSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Order.objects.filter()
    http_method_names = ["post",]



class OrderView(viewsets.ModelViewSet):

    serializer_class = CheckoutSerializer
    permission_classes = [
        # IsAuthenticated,
    ]
    queryset = Order.objects.all()
    http_method_names = ["get","post","patch"]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        user = User.objects.filter(id = instance.user_id).first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        notify_user(instance)
        return Response(serializer.data)

class BasketView(viewsets.ModelViewSet):

    serializer_class = BasketSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Basket.objects.all()
    http_method_names = ["get", "delete", "post"]

class BasketItemView(viewsets.ModelViewSet):

    serializer_class = BasketItemSerializer
    permission_classes = [
        # IsAuthenticated,
    ]
    queryset = BasketItem.objects.all()
    http_method_names = ["get", "delete", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        basket_data = BasketSerializer(Basket.objects.get(id=serializer.data['basket'])).data
        return Response(basket_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        basket_items = BasketItem.objects.filter(basket=serializer.data['basket'])
        basket_total = 0
        for item in basket_items:
            basket_total +=item.item.selling_price

        Basket.objects.filter(
            id=serializer.data['basket']).update(
            basket_total = basket_total
        )
