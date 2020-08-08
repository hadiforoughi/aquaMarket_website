from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Product, TYPE_CHOICES_VAL, Customer, Slider , ProductImage
import re

# Create your views here.

INDEX_LASTPRODUCT_NUMBER = 2
NUMBER_OF_RELATED_PRODUCT = 3
SEARCH_PAGINATE = 4
CATEGORY_PAGINATE = 4


def phone_Valid(s):
    Pattern = re.compile("(0/91)?[0-9]{11}")
    return Pattern.match(s)


def about(request):
    return render(request, "shop/about.html")


def index(request):
    products = Product.objects.all()
    reef_list = products.filter(category='reef').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    salt_fish_list = products.filter(category='saltwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    fresh_fish_list = products.filter(category='freshwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    supplies_list = products.filter(category='supplies').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    offer_products_list = products.filter(has_offer=1).order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    if request.method == "POST":
        phone = request.POST.get('phone')
        if phone is not None:
            if (len(phone) > 6 and len(phone) < 12 and phone_Valid(phone)):
                # has_phone = True
                if (not Customer.objects.filter(phone=phone).exists()):
                    Customer.objects.create(phone=phone)

    return render(request,
                  'shop/index.html',
                  {'reef_list': reef_list,
                   'salt_fish_list': salt_fish_list,
                   'fresh_fish_list': fresh_fish_list,
                   'supplies_list': supplies_list,
                   'offer_products_list': offer_products_list
                   })


class ProductCategory(ListView):
    model = Product
    template_name = 'shop/category.html'
    paginate_by = CATEGORY_PAGINATE

    def get_queryset(self):
        self.category = self.kwargs['category']
        category_product = self.model.objects.filter(category=self.category)
        if len(category_product) == 0:
            return self.model.objects.filter(type=self.category)
        else:
            return category_product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategory, self).get_context_data(**kwargs)
        context['product_category'] = self.category
        if self.category == "supplies" or self.category in TYPE_CHOICES_VAL:
            context['has_type'] = True
        else:
            context['has_type'] = False
        return context


class ProductSearch(ListView):
    model = Product
    template_name = "shop/product_search.html"

    def get_queryset(self):
        query = self.request.GET.get("Search")
        self.queris = self.request.GET
        if query:
            self.product = Product.objects.filter(title__icontains=query)
            # check product exist
            try:
                self.product[0]
                self.not_found = False
                self.paginate_by = SEARCH_PAGINATE
                return self.product
            except IndexError:
                self.not_found = True

        else:
            return Product.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearch, self).get_context_data(**kwargs)
        s = str(self.request.get_full_path())
        if s.__contains__("&page"):
            context['full_path'] = self.request.get_full_path()[0:s.index("&page")]
        else:
            context['full_path'] = self.request.get_full_path()
        context['not_found'] = self.not_found
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "shop/product_detail.html"

    def get_queryset(self):
        self.slug = self.kwargs['slug']
        self.product = Product.objects.filter(slug=self.slug)
        return self.product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        related_products = Product.objects.filter(category=self.get_object().category).order_by('created_time')[
                           0:NUMBER_OF_RELATED_PRODUCT]
        related_list = list(related_products)
        images = ProductImage.objects.filter(product=self.product[0])
        if self.get_object() in related_products:
            related_list.remove(self.get_object())
        context['related_products'] = related_list
        context['images'] = images
        return context
