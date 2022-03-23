from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductOffer, ProductPrice


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def show_all_products_view(request, *args, **kwargs):
    offers = ProductOffer.objects.order_by('product').distinct().all()
    return render(request, 'show-all.html', {'offers': offers})

def show_product_view(request, num, *args, **kwargs):
    product = Product.objects.get(pk=num)
    offers = ProductOffer.objects.filter(product=product)
    prices = ProductPrice.objects.filter(product_offer__in=offers)
    return render(request, 'show-specific.html', {'product': product, 'offers': offers, 'prices': prices})

@api_view(['POST'])
def add_product(request):

    for obj in request.data:

        if Product.objects.filter(code=obj['code']).exists():
            prod = Product.objects.filter(code=obj['code'])[0]

            # product and offer exist, adding current price
            if ProductOffer.objects.filter(product=prod.id, shop=obj['shop']).exists():
                offer = ProductOffer.objects.get(product=prod.id, shop=obj['shop'])
                price = ProductPrice(price=obj['price'], date=obj['date'], product_offer=offer)
                price.save()

            # product exists, adding offer and price
            else:
                offer = ProductOffer(link=obj['link'], image=obj['image'], shop=obj['shop'], product=prod)
                offer.save()
                price = ProductPrice(price=obj['price'], date=obj['date'], product_offer=offer)
                price.save()

        else:
            prod = Product(code=obj['code'], name=obj['name'])
            prod.save()
            offer = ProductOffer(link=obj['link'], image=obj['image'], shop=obj['shop'], product=prod)
            offer.save()
            price = ProductPrice(price=obj['price'], date=obj['date'], product_offer=offer)
            price.save()


    return Response({"message": "OK"})
