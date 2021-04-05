from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(Option)
