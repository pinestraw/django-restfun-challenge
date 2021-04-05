from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

from core import views

urlpatterns = [
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),  # <-- And here
    path("register/", views.UserCreateApiView.as_view(), name="register"),
]
