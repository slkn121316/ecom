from django.contrib import admin
from .models import *
# Register your models here.
class Product_Image_Admin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price']
    inlines = [Product_Image_Admin]



admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)