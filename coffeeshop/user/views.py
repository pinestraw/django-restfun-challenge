from django.contrib.auth import user_logged_out
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from coffeeshop.permissions import IsAnonymous, IsOwner
from .serializers import AuthSerializer, UserSerializer


class AuthView(GenericAPIView):
    """
    #Authentication endpoint.#
    *Returns token if credentials provided are valid*

    **POST request example:**

        * /api/v1/login

            {
                "username": "test1",
                "password": "1234567a",
            }

    **Response example:**

        {
            "token":"25c5c4bcc7a667d910548f3d601f4da5696b2801",
            "user_id":1
        }

    ## Fields legend: ##

        * username - string (required)
        * password - string (required)
    """

    permission_classes = [IsAnonymous]
    serializer_class = AuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        raise serializers.ValidationError(serializer.errors)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        # Logout ENDPOINT #
        ** NOTE ** Send GET request with auth token.
        **NOTE** Wih this request, old token will be deleted.
        So, You'll have to login again to get a new token.
        :param request:
        :return: 200 ok
        """
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )

        return Response({"details": "You are Logged Out"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """
    #User CRUD endpoint#
    **Endpoint to Create, Retrieve, Update, Destroy user instance.**

    **POST (Create): /api/v1/users **

        {
          "username": "test",
          "email": "test@test.com",
          "first_name": "test",
          "last_name": "test"
          "password": "test@12345",
          "confirm_password": "test@12345"
        }

    **GET (Retrieve): /api/v1/users/1**

        {
          "id": 1,
          "username": "test",
          "first_name": "test",
          "last_name": "test",
          "email": "test@test.com",
          "token": "265225ce32997aafe91e2956395e5f1188f241b9"
        }

    **PUT (Update all fields): /api/v1/users/1**

        {
          "username": "abc",
          "first_name": "abc",
          "last_name": "abc",
          "email": "abc@abc.com",
          "password": "abc12345",
          "confirm_password": "abc12345",
          "current_password": "abc1234567"
        }

    ** PATCH for Password Change : **

        {
          "current_password": "string",
          "password": "string"
        }

    ## Fields Legend: ##

        * username - "string"
        * current_password - "string" <- required when user wants to change the email or password
        * password - "string" <- require when user wants to register and change password
        * email - "string"
        * first_name - "string"
        * last_name - "string"

    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def list(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            queryset = self.get_queryset().filter(pk=request.user.id)
            queryset = self.filter_queryset(queryset=queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response([])
