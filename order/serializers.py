from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("product", "options")

    def validate(self, attrs):
        product = attrs.get("product")
        options = attrs.get("options")
        if (options or product.options.all()) and (
            options not in product.options.all()
        ):
            raise ValidationError("please select valid option")
        return attrs


class OrderItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ("order", "id")


class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ("status", "items", "id", "amount")
        extra_kwargs = {"id": {"read_only": True}, "amount": {"read_only": True}}

    def validate(self, attrs):
        attrs = super(OrderWriteSerializer, self).validate(attrs)
        return attrs

    def validate_items(self, value):
        if not value:
            raise ValidationError("please select items")
        return value

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(**validated_data, amount=0)
        for item in items:
            OrderItem.objects.create(order=order, **item, price=item["product"].price)
        order.amount = order.items.aggregate(Sum("price"))["price__sum"]
        order.save()
        return order

    def update(self, instance, validated_data):
        items = validated_data.pop("items")
        instance.items.all().delete()
        for item in items:
            OrderItem.objects.create(
                order=instance, **item, price=item["product"].price
            )
        instance.amount = instance.items.aggregate(Sum("price"))["price__sum"]
        instance.save()
        return instance


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "status", "amount", "items")
