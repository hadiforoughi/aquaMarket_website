from .models import Shop,ShopNumber

def base_context(request):
    shop=Shop.objects.all()
    shop_number=ShopNumber.objects.all()
    return {'shop':shop,'shop_number':shop_number}