from django.test import TestCase
from .models import *
from .serializers import *
from .apis import *
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

class OrderTest(TestCase):

    def setUp(self):
        # Define an user
        user = User.objects.create(
            username='testeuser',
            email='testeuser@tester.com',
            password='#$@123'
        )
        # Create token for the user
        token  = Token.objects.create(user=user)
        
        # Retrieve the default Status
        status = StatusOrder.objects.get(description='Waiting')

        # Delete all orders from this user
        order = Order.objects.filter(user=user)
        order.delete()
        
        # Create an order
        order = Order.objects.create(user=user, consume_location='T', status=status)
        
        # Add items to the order
        product = Product.objects.get(description='Cappuccino')
        option_attribute = OptionAttribute.objects.get(option__description='large', attribute__description='Size')
        item = OptionAttributeProduct.objects.get(product=product, option_attribute=option_attribute)
        order_item = OrderItem.objects.create(order=order, attribute=item, quantity=2, product=product)
        
        product = Product.objects.get(description='Cappuccino')
        option_attribute = OptionAttribute.objects.get(option__description='medium', attribute__description='Size')
        item = OptionAttributeProduct.objects.get(product=product, option_attribute=option_attribute)
        order_item = OrderItem.objects.create(order=order, attribute=item, quantity=1, product=product)

    def test_get_order(self):
        # Define an user
        user = User.objects.get(username='testeuser')

        # Get API response
        factory = APIRequestFactory()
        request = factory.get('api/v1/order')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)

        data_expected = {
            "consume_location": "T",
            "products": [                
                {
                    "product": 2,
                    "attribute": 6,
                    "quantity": 2
                },
                {
                    "product": 2,
                    "attribute": 5,
                    "quantity": 1
                }
            ],
            "price": 30.0,
            "status": "Waiting"
        }
        
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

        order = Order.objects.filter(user=user, status__description='Waiting')
        self.assertEqual(len(order), 1, 'The number of Waiting order should be always 1')    
        
    def test_post_order(self):
        # Define an user
        user = User.objects.get(username='testeuser')

        # Delete all orders from this user
        order = Order.objects.filter(user=user)
        order.delete()

        # Post API - creating orders - Wrong product code
        factory = APIRequestFactory()
        request = factory.post('api/v1/order', {
            "consume_location" : "T",
            "products" : [
                {
                    "product" : -1,
                    "attribute" : 1,
                    "quantity" : 2
                },
                {
                    "product" : 4,
                    "quantity" : 3
                }		
            ]
        }, format='json')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Passed an invalid Product ID')
        
        order = Order.objects.filter(user=user)
        self.assertEqual(len(order),0, 'Order should be empty')

        detail = {
            "consume_location" : "T",
            "products" : [
                {
                    "product" : 1,
                    "attribute" : 1,
                    "quantity" : 2
                },
                {
                    "product" : 4,
                    "quantity" : 3
                }		
            ]
        }

        # Create an order
        request = factory.post('api/v1/order', detail, format='json')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'The order should created successfully')    
        
        # Try to create a new order
        request = factory.post('api/v1/order', detail, format='json')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'The user cannot create a new waiting order')    
        
        # Start order to create a new one
        order = Order.objects.get(user=user, status__description='Waiting')
        order.status = StatusOrder.objects.get(description='Preparation')
        order.save()
        request = factory.post('api/v1/order', detail, format='json')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)        
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'The order should created successfully')    
        
        order = Order.objects.filter(user=user, status__description='Waiting')
        self.assertEqual(len(order),1, 'Order should be not empty')

        order = Order.objects.filter(user=user)
        self.assertEqual(len(order), 2, 'Orders should be more than one')

    def test_put_order(self):
        # Define an user
        user = User.objects.get(username='testeuser')
        
        # Post API - creating orders - Wrong product code
        factory = APIRequestFactory()
        request = factory.put('api/v1/order', {
            "consume_location" : "T",
            "products" : [
                {
                    "product" : 1,
                    "attribute" : 1,
                    "quantity" : 5
                },
                {
                    "product" : 4,
                    "quantity" : 3
                }		
            ]
        }, format='json')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'The order should be updated')    
        
        order = Order.get_current(user=user)
        self.assertEqual(order.price(), 80.0, 'Order price should be 80.0')
    
    def test_delete_order(self):
        # Define an user
        user = User.objects.get(username='testeuser')
        
        # Post API - creating orders - Wrong product code
        factory = APIRequestFactory()
        request = factory.delete('api/v1/order')
        force_authenticate(request, user=user)
        view = OrderApi.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'The order should be deleted')    
        
        order = Order.objects.filter(user=user)
        self.assertEqual(len(order),0, 'Order should be empty')