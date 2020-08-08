from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from .assist import IntegerRangeField
import unidecode
# Create your models here.

CATEGORY_CHOICES=(
    ("saltwater_fish","ماهی آب شور"),
    ("freshwater_fish","ماهی آب شیرین"),
    ("supplies","وسایل و تجهیزات"),
    ("reef","ریف")
)

TYPE_CHOICES={
    ("food","غذا"),
    ("air_pump","پمپ هوا"),
}
TYPE_CHOICES_VAL=["food","air_pump"]

class Shop(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(blank=True)
    addres=models.CharField(max_length=150)
    telegram_link=models.URLField(blank=True)
    instagram_link=models.URLField(blank=True)
    open_time = models.CharField(blank=True,max_length=15)
    def __str__(self):
        return self.name

class ShopNumber(models.Model):
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name="shop_number")
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.shop.name


class Product(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500, blank=True)
    category= models.CharField(max_length=30,choices=CATEGORY_CHOICES)
    created_time=models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100,blank=True, null=True,allow_unicode=True)
    image=models.ImageField(upload_to="shop/image_product",blank=True)
    brand=models.CharField(max_length=100,blank=True)
    orginal_price=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    final_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    rate=IntegerRangeField(min_value=0, max_value=5,blank=True,null=True)
    type=models.CharField(max_length=100,blank=True,choices=TYPE_CHOICES)
    has_offer=models.BooleanField()
    exist=models.BooleanField()

    def save(self, *args, **kwargs):
        if self.slug is None:
            string=self.title.replace(" ","_")
            self.slug = string
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImage (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.TextField(max_length=20)
    image = models.ImageField(upload_to="shop/image_product")

    def __str__(self):
        return self.title + '   ('+self.product.title + ')'

class Customer(models.Model):
    phone = models.CharField(max_length=11,default=00000000000)

    def __str__(self):
        return self.phone

class Slider(models.Model):
    image=models.ImageField(upload_to="shop/image_slider")
    url=models.TextField(blank=True,max_length=50)