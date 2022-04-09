import io, base64
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductOffer, ProductPrice
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def show_all_products_view(request, *args, **kwargs):
    offers = ProductOffer.objects.order_by('product').distinct().all()
    paginator = Paginator(offers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show-all.html', {"page_obj": page_obj})

def show_product_view(request, num, *args, **kwargs):
    product = Product.objects.get(pk=num)
    offers = ProductOffer.objects.filter(product=product)
    prices = ProductPrice.objects.filter(product_offer__in=offers)
    charts = []
    for offer in offers:
        pp = ProductPrice.objects.filter(product_offer=offer)
        prices_list = [x.price for x in pp]
        dates_list = [x.date for x in pp]
        fig, ax = plt.subplots(figsize=(10,3))
        ax = plt.plot(dates_list, prices_list)
        flike = io.BytesIO()
        fig.savefig(flike)
        charts.append(base64.b64encode(flike.getvalue()).decode())
    return render(request, 'show-specific.html', {'product': product, 'offers': offers, 'prices': prices, 'charts': charts})

@api_view(['POST'])
def add_product(request):

    for obj in request.data:

        if Product.objects.filter(code=obj['code']).exists():
            prod = Product.objects.filter(code=obj['code'])[0]

            # product and offer exist, adding current price
            if ProductOffer.objects.filter(product=prod.id, shop=obj['shop']).exists():
                offer = ProductOffer.objects.get(product=prod.id, shop=obj['shop'])
                price = ProductPrice(price=obj['price'].replace(',', '.'), date=obj['date'], product_offer=offer)
                price.save()

            # product exists, adding offer and price
            else:
                offer = ProductOffer(link=obj['link'], image=obj['image'], shop=obj['shop'], product=prod)
                offer.save()
                price = ProductPrice(price=obj['price'].replace(',', '.'), date=obj['date'], product_offer=offer)
                price.save()

        else:
            prod = Product(code=obj['code'], name=obj['name'])
            prod.save()
            offer = ProductOffer(link=obj['link'], image=obj['image'], shop=obj['shop'], product=prod)
            offer.save()
            price = ProductPrice(price=obj['price'].replace(',', '.'), date=obj['date'], product_offer=offer)
            price.save()


    return Response({"message": "OK"})
