from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'attribute', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    consume_location = serializers.CharField(max_length=1, required=True)
    products = OrderItemSerializer(many=True, required=True)
    price    = serializers.FloatField(required=False)
    status   = serializers.CharField(required=False)
    class Meta:
        model = Order
        exclude = ['user']

    def save(self, user):
        # First create the order
        order = Order()
        order.user             = user
        order.consume_location = self.validated_data['consume_location']
        order.status           = StatusOrder.objects.get(description='Waiting')
        order.save()

        # Add items to the order
        for product in self.validated_data['products']:
            order_item          = OrderItem()
            order_item.order    = order
            order_item.product   = product['product']
            order_item.attribute = product.get('attribute', None)
            order_item.quantity  = product['quantity']
            order_item.save()

    def update(self, order):
        # First create the order
        order.consume_location = self.validated_data['consume_location']
        order.save()

        # Clean all order items
        order_item = OrderItem.objects.filter(order=order)
        order_item.delete()

        # Add items to the order
        for product in self.validated_data['products']:
            order_item          = OrderItem()
            order_item.order    = order
            order_item.product   = product.get('product', None)
            order_item.attribute = product.get('attribute', None)
            order_item.quantity  = product.get('quantity', 1)
            order_item.save()