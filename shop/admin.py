from django.contrib import admin
from .models import Shop,ShopNumber,Product,Customer

# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopNumber)
admin.site.register(Product)
admin.site.register(Customer)