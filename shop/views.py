from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import Product,TYPE_CHOICES,Customer
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
                   'has_email':has_email
                   })

class ProductCategory(ListView):
    model = Product
    template_name = 'shop/catagori.html'
    paginate_by = 1
    def get_queryset(self):
        self.category=self.kwargs['category']
        return self.model.objects.filter(category=self.category)
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(ProductCategory,self).get_context_data(**kwargs)
        context['product_category'] = self.category
        if self.category == "supplies":
            context['has_type'] = True
            types=[]
            for item in TYPE_CHOICES:
                types.append(item[1])
            context['types']= types
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
        return Product.objects.filter(slug=self.slug)


