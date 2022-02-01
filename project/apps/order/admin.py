from django.contrib import admin
from project.apps.order.models import Basket,BasketItem, Order, Address


class BasketAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = (
        "id",
        "basket_total",
        "status",
    )
    search_fields = [
        "id"
    ]


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = (
        "order_number",
        "order_total",
        "status",
    )
    search_fields = [
        "id"
    ]

# Register your models here.
admin.site.register(BasketItem)
admin.site.register(Basket,BasketAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Address)