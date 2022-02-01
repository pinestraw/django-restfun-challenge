from django.contrib import admin
from .models import Product, ProductOption, ProductOptionValue, ProductOrder


class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    inlines = [ProductOptionValueInline]
    list_display = ("id", "name")


@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ("id", "option", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(ProductOrder)
class ProductOrder(admin.ModelAdmin):
    list_display = ("id", "product", "status")
