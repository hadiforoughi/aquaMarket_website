from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.index, name="index"),
    path('category/<str:category>', views.ProductCategory.as_view(), name="product_category"),
]
