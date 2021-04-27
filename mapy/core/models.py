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

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

class UserProfile(models.Model):
    user = models.OneToOneField(
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"user: {self.user.username}; token: {self.token}"

class Region(models.Model):
    region = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.region}"

class Category(models.Model):
    category = models.CharField(max_length=100)
    categoryPhoto = models.FileField(upload_to='categories')
    def __str__(self):
        return f"{self.category}"

class SubCategory(models.Model):
    subcategory = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.subcategory}"

class Community(models.Model):
    community = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.community}"

class Artist(models.Model):
    artistName = models.CharField(max_length=100)
    artistPhoto = models.FileField(upload_to='profile_pics')
    artistRegion = models.ForeignKey(Region, on_delete=models.CASCADE)
    artistCommunity = models.ForeignKey(Community, on_delete=models.CASCADE)
    artistText = models.TextField()
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    long = models.DecimalField(max_digits=10, decimal_places=7)

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
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

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


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cartheader = models.ForeignKey(CartHeader,
                             on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=100)
    phone_number = models.DecimalField(max_digits=64,decimal_places=0)
    instructions = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Address: {self.street_address}, {self.shipping_zip}, {self.country}. Phone Number: {self.phone_number}. Instructions: {self.instructions}"

class Payment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    holder_name = models.CharField(max_length=100)
    card_number = models.IntegerField()
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class About(models.Model):
    title = models.TextField(max_length=100)
    firstContent = models.TextField(max_length=5000)
    subtitle = models.TextField(max_length=100)
    secondContent = models.TextField(max_length=5000)
    contentPhoto = models.FileField(upload_to='about_photo')

    def __str__(self):
        return self.title

class TeamMemeber(models.Model):
    name = models.TextField(max_length=100)
    job = models.TextField(max_length=100)
    email = models.EmailField()
    profile = models.FileField(upload_to='profile')

    def __str__(self):
        return f'{self.name} {self.job}'

class FAQ(models.Model):
    question = models.TextField(max_length=100)
    answer = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.question} {self.answer}'
