from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.index, name="index"),
    path('category/<str:category>', views.ProductCategory.as_view(), name="product_category"),
    path('about/', views.about, name="about"),
    path('search/', views.ProductSearch.as_view(), name="product_search"),
    path('product/<str:slug>/', views.ProductDetails.as_view(), name="product_detail")

]
