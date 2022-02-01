from rest_framework import serializers
from django.core import serializers as core_serializers
from .models import Product,ProductsAttributeValue
import json

# class ChildNavigationSerializer(serializers.ModelSerializer):
#     product_attribute = serializers.SerializerMethodField(read_only=True)

#     def get_product_attribute(self, obj):
#         attributes ={}
#         qs = ProductsAttributeValue.objects.filter(
#             product= obj
#         )
#         key = qs.first().attribute
#         value = qs.first().value_option.all()
#         # attributes[str(key)] = 
#         print(key)
#         print(value)
#         return attributes
#     class Meta:
#         model = Product
#         fields = ('id','title','selling_price','discount_price','cost_price','stock','is_available','slug','description','product_type','product_attribute')
#         depth = 1

class ProductSerializer(serializers.ModelSerializer):
    product_attribute = serializers.SerializerMethodField(read_only=True)

    def get_product_attribute(self, obj):
        attributes ={}
        qs = ProductsAttributeValue.objects.filter(
            product= obj
        )
        if qs.exists():
            key = qs.first().attribute
            values=[value[0] for value in qs.first().value_option.all().values_list('option')]
            attributes[str(key)] = values    
            return attributes
        
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1 

