from django.urls import path
from .views import *

urlpatterns = [
    path('register/',viewregister,name='register'),
    path('login/',viewlogin,name='login'),
    path('logout/', logout_view, name='logout'),

    path('activate/<email_token>',activate_email,name='activate'),

    path('cart/',cartview, name='cart'),
    
    # Update quantity AJAX endpoint
    # path('cart/update_quantity/', update_quantity, name='update_quantity'),
    # path('cart/', cart_page, name='cart_page'),
    # path('cart/update_quantity/', update_quantity, name='update_quantity'),
    # path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<str:product_uid>/', add_to_cart, name='add_to_cart'),
    # path('update_cart/', update_cart, name='update_cart'),
    # path('order-summary/', order_summary, name='order_summary'),
    

    # path('add-to-cart/product.id/', add_to_cart, name='add_to_cart'),
    # path('add_to_cart/<str:product_uid>/', add_to_cart, name='add_to_cart'),
    # path('add_to_cart_anonymous/<str:product_uid>/', add_to_cart_anonymous, name='add_to_cart_anonymous'),
    # path('cart/', cart_view, name='cart_view'),
    # path('cart/anonymous/', cart_view_anonymous, name='cart_view_anonymous'),

]