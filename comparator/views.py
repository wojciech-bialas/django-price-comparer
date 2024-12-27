import io, base64
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductOffer, ProductPrice, ObservedProducts, DatesWhenScraperRun
from .utils import Chart
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import date


def home_view(request, *args, **kwargs):
    charts = Chart().make_all_cat_charts()
    return render(request, 'home.html', {"charts": charts})

def search_view(request, *args, **kwargs):
    if not request.GET.get('query'):
        return render(request, 'search.html', {"page_obj": []})
    p = Product.objects.filter(name__icontains=request.GET.get('query'))
    results = ProductOffer.objects.filter(product__in=p)
    paginator = Paginator(results, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'search.html', {"page_obj": page_obj}) 

def show_gpu_view(request, *args, **kwargs):
    offers = ProductOffer.objects.filter(product__category='gpu')
    paginator = Paginator(offers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show-all.html', {"page_obj": page_obj})

def show_cpu_view(request, *args, **kwargs):
    offers = ProductOffer.objects.filter(product__category='cpu')
    paginator = Paginator(offers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show-all.html', {"page_obj": page_obj})

def show_ram_view(request, *args, **kwargs):
    offers = ProductOffer.objects.filter(product__category='ram')
    paginator = Paginator(offers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'show-all.html', {"page_obj": page_obj})

def show_product_view(request, num, *args, **kwargs):
    product = Product.objects.get(pk=num)
    offers = ProductOffer.objects.filter(product=product)
    prices = ProductPrice.objects.filter(product_offer__in=offers)
    charts = [
        Chart().get_product_chart(offer) for offer in offers
    ]
    observed = None
    if request.user.is_authenticated:
        observed = ObservedProducts.objects.filter(user=request.user, product=product).exists()

    return render(request, 'show-specific.html', {'product': product, 'offers': offers, 'prices': prices, 'charts': charts, 'observed': observed})

def observe_view(request, num):
    prod = Product.objects.get(pk=num)
    try:
        obs = ObservedProducts.objects.get(
            Q(user=request.user) & Q(product=prod)
        )
    except ObjectDoesNotExist:
        # if product is not observed - observe it
        user = request.user
        price = ProductPrice.objects.filter(product_offer__product=prod).last().price
        obs = ObservedProducts(user=user, product=prod, price=price)
        obs.save()
    else:
        # if product is observed - unobserve it
        obs = ObservedProducts.objects.get(
            Q(user=request.user) & Q(product=prod)
        ).delete()
    return redirect('show-specific', num=num)

def user_observed_view(request):
    observed = list(ObservedProducts.objects.filter(user=request.user).values_list('product', flat=True))
    products = Product.objects.filter(pk__in=observed)
    offers = ProductOffer.objects.filter(product__in=products)
    prices = ProductPrice.objects.filter(product_offer__in=offers)
    observed_prices = ObservedProducts.objects.filter(
        Q(user=request.user) & Q(product__in=products)
    )
    paginator = Paginator(offers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'observed.html', {"page_obj": page_obj})

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
            prod = Product(code=obj['code'], name=obj['name'], category=obj['category'])
            prod.save()
            offer = ProductOffer(link=obj['link'], image=obj['image'], shop=obj['shop'], product=prod)
            offer.save()
            price = ProductPrice(price=obj['price'].replace(',', '.'), date=obj['date'], product_offer=offer)
            price.save()
    
    if not DatesWhenScraperRun.objects.filter(date=date.today().strftime("%Y-%m-%d")):
        DatesWhenScraperRun(date=date.today().strftime("%Y-%m-%d")).save()

    return Response({"message": "OK"})
