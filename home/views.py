from django.shortcuts import render
from products.models import *

# Create your views here.


def index(request):
    categories = Category.objects.all()
    products_by_category = {}

    for category in categories:
        products = Product.objects.filter(category=category)
        products_by_category[category] = products

    context = {'products_by_category': products_by_category}
    
    return render(request, 'home/example.html', context)