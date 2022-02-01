from itertools import product
from statistics import mode
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
class AttributeOptionGroup(models.Model):

    name = models.CharField(_('Name'), max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "catalogue"
        db_table = "AttributeOptionGroup"
        verbose_name = "AttributeOptionGroup"
        verbose_name_plural = "AttributeOptionGroups"

    @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)

class AttributeOption(models.Model):

    group = models.ForeignKey(
        'catalogue.AttributeOptionGroup',
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)

    def __str__(self):
        return self.option

    class Meta:
        app_label = "catalogue"
        db_table = "AttributeOption"
        verbose_name = "AttributeOption"
        verbose_name_plural = "AttributeOptions"


class ProductType(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "catalogue"
        db_table = "ProductType"
        verbose_name = "ProductType"
        verbose_name_plural = "ProductTypes"


class ProductAttribute(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True,blank=True)
    option_group = models.ForeignKey(AttributeOptionGroup,on_delete=models.CASCADE,max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    parent = models.ForeignKey('self',models.CASCADE,null=True,blank=True)
    LABEL_CHOICES = (
        ('S', 'Standalone'),
        ('P', 'Parent'),
        ('C', 'Child')
    )

    title = models.CharField(max_length=100)
    selling_price = models.FloatField(null=True,blank=True)
    discount_price = models.FloatField(blank=True, null=True)
    cost_price = models.FloatField(null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE, null=True,blank=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        app_label = "catalogue"
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductsAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    value_option = models.ManyToManyField(AttributeOption)