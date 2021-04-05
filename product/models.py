from django.db import models

# Create your models here.


class Option(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductOption(models.Model):
    name = models.CharField(max_length=255)
    option = models.ForeignKey(
        "Option", related_name="options", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    options = models.ManyToManyField("ProductOption", blank=True)

    def __str__(self):
        return self.name
