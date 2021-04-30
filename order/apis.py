from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status

"""
View to order actions

* Requires token authentication.
"""
class OrderApi(APIView):    
    permission_classes = (
     IsAuthenticated,)

    def post(self, request):
        order = Order.get_current(user=request.user)
        if order._state.adding is False:
            return JsonResponse({'message' : 'There is a waiting order for the user'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            try:
                order_serializer.save(request.user)
            except:
                return JsonResponse({'message' : 'Error creating the order'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
            return JsonResponse(None, safe=False)
        
        return JsonResponse({'message' : order_serializer.errors}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def put(self, request):
        order = Order.get_current(user=request.user)
        if order._state.adding:
            return JsonResponse({'message' : 'There isn`t any waiting order for the user'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
        if order.status != StatusOrder.objects.get(description='Waiting'):
            return JsonResponse({'message' : 'The order is not available to any change'}, status=status.HTTP_400_BAD_REQUEST, safe=False)

        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            try:
                order_serializer.update(order)
            except:
                return JsonResponse({'message' : 'Error updating the order'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
            return JsonResponse(None, safe=False)
        
        return JsonResponse({'message' : order_serializer.errors}, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request):
        order = Order.get_current(user=request.user)
        if order._state.adding:
            return JsonResponse({'message' : 'There is no waiting order for the user'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
        try:
            order.delete()
            return JsonResponse(None, safe=False)
        except:
            return JsonResponse({'message' : 'Error deleting the order'}, status=status.HTTP_400_BAD_REQUEST, safe=False)


    def get(self, request):        
        order = Order.get_current(user=request.user)        
        if order._state.adding:
            return JsonResponse({'message' : 'There isn`t any waiting order for the user'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
        
        order_data = {}
        order_data['consume_location'] = order.consume_location

        products = OrderItem.objects.filter(order=order)
        order_data['products'] = [{
            'attribute' : (product.attribute.pk if product.attribute else None), 
            'quantity' : product.quantity,
            'product' : product.product.pk} for product in products]

        order_data['price']  = order.price()
        order_data['status'] = order.status.description
        
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            return JsonResponse(order_serializer.data, safe=False)
        else:
            return JsonResponse({'message' : order_serializer.errors}, status=status.HTTP_400_BAD_REQUEST, safe=False)

