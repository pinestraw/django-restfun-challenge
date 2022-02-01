from django.contrib import admin

# Register your models here.
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    list_display = ("status", "amount", "user")


admin.site.register(Order, OrderAdmin)
