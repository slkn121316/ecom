from django.shortcuts import render
from .models import Product
from accounts.models import *
from django.http import HttpResponseRedirect

# Create your views here.

def product_details(request,slug):
    product=Product.objects.get(slug=slug)
    cate_products = Product.objects.filter(category=product.category)
    d1 = {"product":product,'cate_products':cate_products}
    return render(request,'products/product_details.html',context=d1)
