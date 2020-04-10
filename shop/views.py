from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

INDEX_LASTPRODUCT_NUMBER = 2


def index(request):
    products = Product.objects.all()
    reef_list = products.filter(category='reef').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    salt_fish_list = products.filter(category='saltwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    fresh_fish_list = products.filter(category='freshwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    supplies_list = products.filter(category='supplies').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    offer_products_list = products.filter(has_offer=1).order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]

    return render(request,
                  'shop/index.html',
                  {'reef_list': reef_list,
                   'salt_fish_list': salt_fish_list,
                   'fresh_fish_list': fresh_fish_list,
                   'supplies_list': supplies_list,
                   'offer_products_list': offer_products_list,
                   })
