from django.urls import path
from .apis import *

urlpatterns = [
    path('', ProductApi.as_view()),
]