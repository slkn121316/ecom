from django.db import models
from base.models import Basemodel
from base.email import send_account_activation_email
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from products.models import *


# Create your models here.

class Profile(Basemodel):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def __str__(self):
        return self.user.username

    def email(self):
        return self.user.email


class ShippingAddress(Basemodel):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.address



class Cart(Basemodel):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Additional fields or methods

    def __str__(self):
        return f"Cart for {self.user.first_name} - {self.product.product_name}"







@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance,email_token=email_token)
            email = instance.email
            send_account_activation_email(email,email_token)

    except Exception as e:
        print(e)

