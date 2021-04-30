from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

"""
View to list all products

* Requires token authentication.
"""
class ProductApi(APIView):    
    permission_classes = (
     IsAuthenticated,)
    def get(self, request):
        """
        Return a list of all products
        """
        products   = Product.objects.all()
        products_  = []
        for product in products:
            data_product = {}
            data_product['description'] = product.description
            data_product['id_product']  = product.pk
            data_product['attributes']  = {}
            # Get product attributes
            product_details = OptionAttributeProduct.objects.select_related('option_attribute').filter(product=product)
            for option in product_details:
                detail = {
                    'id_optionattribute_product' : option.option_attribute.option.pk,
                    'description' : option.option_attribute.option.description,
                }
                if option.option_attribute.attribute.description in data_product['attributes']:
                    data_product['attributes'][option.option_attribute.attribute.description].append(detail)
                else:
                    data_product['attributes'][option.option_attribute.attribute.description] = [detail]
            products_.append(data_product)
            

        return JsonResponse(data=products_, safe=False)
