from django.urls import path

from product import views

urlpatterns = [
    path("list/", views.ProductListApiView.as_view(), name="product-list"),
]
