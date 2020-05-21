from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import Product,TYPE_CHOICES_VAL,Customer,Slider
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

INDEX_LASTPRODUCT_NUMBER = 2
NUMBER_OF_RELATED_PRODUCT=3


def index(request):
    products = Product.objects.all()
    reef_list = products.filter(category='reef').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    salt_fish_list = products.filter(category='saltwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    fresh_fish_list = products.filter(category='freshwater_fish').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    supplies_list = products.filter(category='supplies').order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    offer_products_list = products.filter(has_offer=1).order_by('created_time')[0:INDEX_LASTPRODUCT_NUMBER]
    slider=Slider.objects.all()
    slider_size=str(len(slider))
    has_email=False
    if request.method == "POST":
        email=request.POST.get('email')
        if email is not None :
            has_email = True
            if (not Customer.objects.filter(email=email).exists()):
                Customer.objects.create(email=email)
    return render(request,
                  'shop/index.html',
                  {'reef_list': reef_list,
                   'salt_fish_list': salt_fish_list,
                   'fresh_fish_list': fresh_fish_list,
                   'supplies_list': supplies_list,
                   'offer_products_list': offer_products_list,
                   'has_email':has_email,
                   'sliders':slider,
                   'slider_size':slider_size
                   })

class ProductCategory(ListView):
    model = Product
    template_name = 'shop/category.html'
    paginate_by = 1
    def get_queryset(self):
        self.category=self.kwargs['category']
        category_product=self.model.objects.filter(category=self.category)
        if len(category_product)==0:
            return self.model.objects.filter(type=self.category)
        else:return category_product
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(ProductCategory,self).get_context_data(**kwargs)
        context['product_category'] = self.category
        if self.category == "supplies" or self.category in TYPE_CHOICES_VAL:
            context['has_type'] = True
        else:
            context['has_type'] = False
        return context



class ProductSearch(ListView):
    model = Product
    template_name = "shop/product_search.html"
    paginate_by = 1
    def get_queryset(self):
        query= self.request.GET.get("Search")
        self.queris=self.request.GET

        if query:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.none()
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(ProductSearch,self).get_context_data(**kwargs)
        context['full_path']=self.request.get_full_path()
        return context

class ProductDetails(DetailView):
    model = Product
    template_name = "shop/product_detail.html"

    def get_queryset(self):
        self.slug=self.kwargs['slug']
        product=Product.objects.filter(slug=self.slug)
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(ProductDetails,self).get_context_data(**kwargs)
        related_products=Product.objects.filter(category=self.get_object().category).order_by('created_time')[0:NUMBER_OF_RELATED_PRODUCT]
        related_list = list(related_products)
        if self.get_object() in related_products :
            related_list.remove(self.get_object())

        context['related_products'] =related_list
        return context

