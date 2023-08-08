from django.urls import path
from .views import *

urlpatterns = [
    path('<slug>/',product_details,name='product_detail')
]