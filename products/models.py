from django.db import models
from base.models import Basemodel
from django.utils.text import slugify

# Create your models here.
class Category(Basemodel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True,blank=True, unique=True)
    category_image = models.ImageField(null=True,blank=True,upload_to='categories')

    def save(self, *args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.category_name


class Product(Basemodel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True,blank=True, unique=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(max_length=1000,default='N/A')
 
    def save(self, *args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.product_name


class ProductImage(Basemodel):
    products = models.ForeignKey(Product , on_delete=models.CASCADE, related_name='product_images')
    image =  models.ImageField(upload_to='product')




