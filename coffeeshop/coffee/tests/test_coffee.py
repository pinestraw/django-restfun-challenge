import pytest
from django.contrib.auth.models import User

from coffee.models import ProductOption, ProductOptionValue, Product, ProductOrder
from coffee.serializers import ProductOrderSerializer

pytestmark = pytest.mark.django_db


def test_add_product_options(input_fixtures):
    option_params = input_fixtures('test_product_options.json')

    for option in option_params:
        product_option = ProductOption.objects.create(name=option['name'])

        assert product_option.name == option['name']

        for value in option['values']:
            option_value = ProductOptionValue.objects.create(option=product_option, value=value)

            assert option_value.option == product_option


def test_add_product(input_fixtures):
    option_params = input_fixtures('test_product_options.json')

    for option in option_params:
        product_option = ProductOption.objects.create(name=option['name'])
        for value in option['values']:
            option_value = ProductOptionValue.objects.create(option=product_option, value=value)

    params = input_fixtures('test_products.json')
    for param in params:
        param['product_option'] = ProductOption.objects.get(id=param['product_option'])
        product = Product.objects.create(**param)

        assert product.name == param['name']

        assert product.product_option.name == param['product_option'].name


def test_add_product_order(input_fixtures):
    option_params = input_fixtures('test_product_options.json')

    for option in option_params:
        product_option = ProductOption.objects.create(name=option['name'])
        for value in option['values']:
            option_value = ProductOptionValue.objects.create(option=product_option, value=value)

    params = input_fixtures('test_products.json')
    for param in params:
        param['product_option'] = ProductOption.objects.get(id=param['product_option'])
        product = Product.objects.create(**param)

    order_params = input_fixtures('test_product_order.json')

    user_data = {
        "username": "test",
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "Test",
        "password": "test@12345",
    }
    user = User.objects.create(**user_data)

    for param in order_params:
        param['user'] = user.id
        serializer = ProductOrderSerializer(data=param)
        assert serializer.is_valid()

        instance = serializer.save()

        assert instance.status == "waiting"

        param['status'] = "canceled"

        serializer = ProductOrderSerializer(instance=instance, data=param)

        assert serializer.is_valid() is True

        instance_1 = serializer.save()

        assert instance_1.status == "canceled"
