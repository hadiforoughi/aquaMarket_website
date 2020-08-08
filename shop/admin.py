from django.contrib import admin
from .models import Shop,ShopNumber,Product,Customer,Slider , ProductImage

# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopNumber)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Slider)
admin.site.register(ProductImage)