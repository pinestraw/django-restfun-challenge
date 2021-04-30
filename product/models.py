from django.db import models

class Product(models.Model):
    description = models.CharField(max_length=150)
    price = models.FloatField(default=10.0)
    def __str__(self):
        return 'Product: %s - Price: $%f' % ( self.description , self.price )

class Attribute(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return 'Attribute: %s' % ( self.description )

class Option(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return 'Option: %s' % ( self.description )

class OptionAttribute(models.Model):
    option    = models.ForeignKey(
        Option,
        on_delete=models.PROTECT)
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.PROTECT)
    def __str__(self):
        return 'An %s from %s' % ( self.option , self.attribute )

class OptionAttributeProduct(models.Model):
    option_attribute = models.ForeignKey(
        OptionAttribute,
        on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT)
    price_perc = models.FloatField(default=1.0)
    def __str__(self):
        return '%s - for %s, price %f' % ( self.option_attribute, self.product, self.price_perc * self.product.price )

