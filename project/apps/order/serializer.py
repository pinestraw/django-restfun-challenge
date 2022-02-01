from rest_framework import exceptions, serializers
from project.apps.order.models import Basket, Address, Order, BasketItem
from project.apps.catalogue.models import ProductsAttributeValue
from project.apps.catalogue.serializers import ProductSerializer

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Address

class BasketItemSerializer(serializers.ModelSerializer):
    item_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        fields = '__all__'
        model = BasketItem

    def get_item_detail(self, obj):
        return ProductSerializer(obj.item).data


class BasketSerializer(serializers.ModelSerializer):
    basket_items = serializers.SerializerMethodField(read_only=True)
    class Meta:
        fields = '__all__'
        model = Basket

    def get_basket_items(self, obj):
        return BasketItemSerializer(BasketItem.objects.filter(basket=obj.id), many=True).data


class CheckoutSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer(read_only=True)
    basket = BasketSerializer()
    class Meta:
        fields = '__all__'
        model = Order

