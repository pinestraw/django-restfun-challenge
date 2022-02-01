from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

class ProductViewset(viewsets.ModelViewSet):
    pagination_class = None
    http_method_names = ["get"]
    queryset = Product.objects.filter( is_available=True, parent__isnull=False)
    serializer_class = ProductSerializer