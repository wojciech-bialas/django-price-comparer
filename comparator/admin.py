from django.contrib import admin
from .models import Product, ProductOffer, ProductPrice, ObservedProducts

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductOffer)
admin.site.register(ProductPrice)
admin.site.register(ObservedProducts)
