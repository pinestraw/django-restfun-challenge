from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from product.models import Product
from product.serializers import ProductSerializer


class ProductListApiView(ListAPIView):
    """
    product list
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
