from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    message = models.TextField(max_length=400)
    thumbnail_url = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    margin = models.DecimalField(max_digits=2, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    stars = models.SmallIntegerField()


class Profile(models.Model):
    user = models.OneToOneField(  settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=40, blank=True)
    last_name = models.TextField(max_length=40, blank=True)
    company = models.TextField(max_length=100, blank=True)
    address_line_one = models.TextField(max_length=100, blank=True)
    address_line_two = models.TextField(max_length=100, blank=True)
    phone =  PhoneNumberField()
    country = CountryField(blank_label='Select a country')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Cart(models.Model):
    quantity =  models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
