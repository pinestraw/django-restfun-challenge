from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Option)
admin.site.register(OptionAttribute)
admin.site.register(OptionAttributeProduct)