from django.contrib import admin

# Register your models here.
from project.apps.catalogue.models import Product, ProductAttribute,AttributeOption, AttributeOptionGroup,ProductType, ProductsAttributeValue



# Register your models here.

class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption


class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]



class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0

class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductAttributeInline]
    extra = 0
class AttributeInline(admin.TabularInline):
    model = ProductsAttributeValue
    extra = 0
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','parent','product_type')
    inlines = [AttributeInline]
    extra = 0


admin.site.register(ProductAttribute)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductType,ProductClassAdmin)
admin.site.register(AttributeOptionGroup,AttributeOptionGroupAdmin)