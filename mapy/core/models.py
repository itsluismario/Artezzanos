from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

class UserProfile(models.Model):
    user = models.OneToOneField(
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Region(models.Model):
    region = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.region}"

class Category(models.Model):
    category = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.category}"

class Community(models.Model):
    community = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.community}"

class Artist(models.Model):
    artistName = models.CharField(max_length=100, blank=False, null=False)
    artistPhoto = models.FileField(upload_to='profile_pics',blank=False)
    artistRegion = models.ForeignKey(Region, on_delete=models.CASCADE)
    artistCommunity = models.ForeignKey(Community, on_delete=models.CASCADE)
    artistText = models.TextField(max_length=1000, blank=False, null=False)
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=False, null=False)
    long = models.DecimalField(max_digits=10, decimal_places=7, blank=False, null=False)

    def __str__(self):
        return f"{self.artistName} from {self.artistRegion}"

class Item(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    video = models.FileField(upload_to='video_products',blank=True)
    itemPhotoComplete = models.FileField(upload_to='photocomplete_products',blank=True)
    itemPhotoZoomIn = models.FileField(upload_to='zoomin_products',blank=True)
    itemPhotoShowRoom = models.FileField(upload_to='showroom_products',blank=True)

    title = models.CharField(max_length=100)
    price = models.IntegerField()
    hours = models.IntegerField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    artType = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.title} by {self.artist}"

class CartHeader(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,null=True)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Id: {self.id}. Total: ${self.total}. Quantity: {self.quantity} items. User: {self.user}"

class CartBody(models.Model):
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    cartHeader = models.ForeignKey(CartHeader,
                             on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    quantityByItems = models.IntegerField()

    def __str__(self):
        return f"Id: {self.id}. carBody of cartHeader {self.cartHeader.id}. Item: {self.item}. Quantity: {self.quantityByItems}"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)

    country = CountryField(multiple=False)

    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
