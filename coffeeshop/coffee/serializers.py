from rest_framework import serializers

from user.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductOption, ProductOptionValue, ProductOrder


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    product_option = ProductOptionSerializer()
    possible_values = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "photo", "product_option", "possible_values"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def get_possible_values(self, obj):
        return obj.product_option.option_values.values("id", "value")


class ProductOrderSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductOrder
        fields = ["id", "product", "option_value", "status", "price", "user"]
        extra_kwargs = {"id": {"read_only": True}, "user": {"required": False}}

    def to_representation(self, instance):
        ret = super(ProductOrderSerializer, self).to_representation(instance)
        option_value = ProductOptionValue.objects.get(id=ret['option_value'])
        ret['option_value'] = {'id': option_value.id, 'value': option_value.value}
        return ret

    def get_price(self, obj):
        return obj.product.price

    def validate(self, attrs):
        if "user" not in attrs:
            attrs["user"] = self.context["request"].user

        option_value = attrs.get("option_value")
        product = attrs.get("product")

        if product:
            if not product.product_option.option_values.filter(
                id=option_value.id
            ).exists():
                raise serializers.ValidationError(
                    {"non_field_errors": [_("Invalid Option Value")]}
                )

        if self.instance:
            if self.instance.status == "canceled":
                raise serializers.ValidationError(
                    {"non_field_errors": [_("Order is already canceled")]}
                )

            if not self.instance.status == "waiting":
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            _("You are now allowed to update or cancel the order")
                        ]
                    }
                )

            if attrs.get("status") and attrs.get("status") != "canceled":
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            _("You are only allowed to update order to Canceled")
                        ]
                    }
                )

        return super(ProductOrderSerializer, self).validate(attrs)
