import pytest
from django.urls import reverse

from user.serializers import UserSerializer

pytestmark = pytest.mark.django_db


def test_add_user():
    data = {
        "username": "test",
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "Test",
        "password": "test@12345",
        "confirm_password": "test@12345",
    }

    serializer = UserSerializer(data=data)
    assert serializer.is_valid() is True

    instance = serializer.save()
    assert instance.username == "test"


# def test_add_user_view(client):
#     data = {
#         "username": "test 1",
#         "email": "test1@test.com",
#         "first_name": "Test 1",
#         "last_name": "Test 1",
#         "password": "test@12345",
#         "confirm_password": "test@12345",
#     }
#
#     response = client.post(reverse("users"), data)
#
#     assert response.status_code == 201

# def test_login_user_view(client):
#     data = {
#         "username": "test",
#         "password": "test@12345"
#     }
#
#     response = client.post(reverse("login"), data)
#
#     assert response.status_code == 200
