from django.test import TestCase
from .models import *
from .serializers import *
from .apis import *
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

class ProductTest(TestCase):

    def setUp(self):
        # Define an user
        user = User.objects.create(
            username='testeuser',
            email='testeuser@tester.com',
            password='#$@123'
        )
        # Create token for the user
        token  = Token.objects.create(user=user)
        
    def test_get_products(self):
        # Define an user
        user = User.objects.get(username='testeuser')

        # Get API response
        factory = APIRequestFactory()
        request = factory.get('api/v1/product')
        force_authenticate(request, user=user)
        view = ProductApi.as_view()
        response = view(request)

        data_expected = [
            {
                "description": "Latte",
                "id_product": 1,
                "attributes": {
                "Milk": [
                    {
                    "description": "skim",
                    "id_optionattribute_product": 1
                    },
                    {
                    "description": "semi",
                    "id_optionattribute_product": 2
                    },
                    {
                    "description": "whole",
                    "id_optionattribute_product": 3
                    }
                ]
                }
            },
            {
                "description": "Cappuccino",
                "id_product": 2,
                "attributes": {
                "Size": [
                    {
                    "description": "small",
                    "id_optionattribute_product": 4
                    },
                    {
                    "description": "medium",
                    "id_optionattribute_product": 5
                    },
                    {
                    "description": "large",
                    "id_optionattribute_product": 6
                    }
                ]
                }
            },
            {
                "description": "Espresso",
                "id_product": 3,
                "attributes": {
                "Shots": [
                    {
                    "description": "single",
                    "id_optionattribute_product": 7
                    },
                    {
                    "description": "double",
                    "id_optionattribute_product": 8
                    },
                    {
                    "description": "triple",
                    "id_optionattribute_product": 9
                    }
                ]
                }
            },
            {
                "description": "Tea",
                "id_product": 4,
                "attributes": {}
            },
            {
                "description": "Hot chocolate",
                "id_product": 5,
                "attributes": {
                "Size": [
                    {
                    "description": "small",
                    "id_optionattribute_product": 4
                    },
                    {
                    "description": "medium",
                    "id_optionattribute_product": 5
                    },
                    {
                    "description": "large",
                    "id_optionattribute_product": 6
                    }
                ]
                }
            },
            {
                "description": "Cookie",
                "id_product": 6,
                "attributes": {
                "Kind": [
                    {
                    "description": "chocolate chip",
                    "id_optionattribute_product": 10
                    },
                    {
                    "description": "ginger",
                    "id_optionattribute_product": 11
                    }
                ]
                }
            }
        ]
        
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
        