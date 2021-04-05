from rest_framework import serializers

from .models import Product, ProductOption


class OptionSerializer(serializers.ModelSerializer):
    option_type = serializers.CharField(source="option.name")

    class Meta:
        model = ProductOption
        fields = ("name", "id", "option_type")


class ProductSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
        depth = 2
