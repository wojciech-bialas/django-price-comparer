from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=250)
    category = models.CharField(max_length=60)

class ProductOffer(models.Model):
    link = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    shop = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductPrice(models.Model):
    price = models.FloatField()
    date = models.DateField()
    product_offer = models.ForeignKey(ProductOffer, on_delete=models.CASCADE)

class ObservedProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()

class DatesWhenScraperRun(models.Model):
    date = models.DateField()
