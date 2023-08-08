from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import  *
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.http import JsonResponse


def viewregister(request):
    if request.method == "GET":
        return render(request, 'accounts/register.html')
    
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.info(request, "Account Already Exists")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "Account Created Successfully")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def viewlogin(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html')

    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, "User Not Found!!!!")
            return HttpResponseRedirect(reverse('login'))

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your Email is Not verified Yet")
            return HttpResponseRedirect(reverse('login'))

        user_obj1 = authenticate(request, username=email, password=password)
        if user_obj1:
            login(request,user_obj1)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credential")
            return HttpResponseRedirect(reverse('login'))

    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def activate_email(request,email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return HttpResponse("<h1>Account Activated Successfully")
    except Exception as e:
        return HttpResponse('<h1>Invalid Email Token</h1>')
    
# def calculate_total_price(cart_items):
#     total_price = 0
#     for item in cart_items:
#         total_price += item.price * item.quantity
#     return total_price


@login_required(login_url='login')
def cartview(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'accounts/cart1.html', {'cart_items': cart_items})


@login_required(login_url='login')
def update_quantity(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        quantity = request.POST.get('quantity')
        cart_item = get_object_or_404(Cart, uid=uid)

        # Update the quantity
        cart_item.quantity = quantity

        # Recalculate the price based on the updated quantity
        cart_item.price = cart_item.product.price * int(quantity)

        # Save the changes
        cart_item.save()

        # Prepare the JSON response
        response_data = {
            'success': True,
            'price': cart_item.price,
        }

        return JsonResponse(response_data)




# @login_required(login_url='login')
# def remove_from_cart(request):
#     if request.method == 'POST':
#         uid = request.POST.get('uid')
#         cart_item = get_object_or_404(Cart, uid=uid)
#         cart_item.delete()

#     return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_to_cart(request, product_uid):
    user = request.user
    product = get_object_or_404(Product, uid=product_uid)

    # Check if the product is already in the user's cart
    cart_item = Cart.objects.filter(user=user, product=product).first()

    if cart_item:
        # Product already exists in the cart, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Product not found in the cart, create a new cart item
        price = product.price
        cart_item = Cart.objects.create(user=user, product=product, price=price)

    return redirect(request.META.get('HTTP_REFERER'))


# from django.views.generic import TemplateView
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Cart

# class CartView(TemplateView):
#     template_name = 'accounts/cart.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         cart_items = Cart.objects.filter(user=user)
#         total_price = sum(item.price for item in cart_items)
#         context['cart_items'] = cart_items
#         context['total_price'] = total_price
#         return context

# def update_quantity(request):
#     if request.method == 'POST' and request.is_ajax():
#         cart_id = request.POST.get('cart_id')
#         quantity = int(request.POST.get('quantity'))

#         try:
#             cart_item = Cart.objects.get(id=cart_id)
#             cart_item.quantity = quantity
#             cart_item.save()
#             return JsonResponse({'success': True})
#         except Cart.DoesNotExist:
#             return JsonResponse({'success': False})

#     return JsonResponse({'success': False})



  

