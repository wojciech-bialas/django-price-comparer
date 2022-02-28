from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=120)

class ProductOffer(models.Model):
    link = models.CharField
    image = models.CharField
    shop = models.IntegerField
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

class ProductPrice(models.Model):
    price = models.FloatField
    date = models.DateField
    product_offer = models.ForeignKey(ProductOffer, on_delete=models.PROTECT)
