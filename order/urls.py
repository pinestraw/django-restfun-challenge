from django.urls import path
from .apis import *

urlpatterns = [
    path('', OrderApi.as_view(), name='orders'),
]