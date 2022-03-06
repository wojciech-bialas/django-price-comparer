from rest_framework import serializers
from comparator.models import Product, ProductOffer, ProductPrice


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('code', 'name')


class ProductOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOffer
        fields = ('link', 'image', 'shop', 'product')


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('price', 'date', 'product_offer')
