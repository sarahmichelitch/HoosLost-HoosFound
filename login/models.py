"""
REFERENCES
Title: Upload Images To Django - Django Wednesdays #38
URL: https://www.youtube.com/watch?v=O5YkEFLXcRg&ab_channel=Codemy.com

Title: Model Field Reference (DecimalField)
URL: https://docs.djangoproject.com/en/4.2/ref/models/fields/

Title: ChatGPT
Prompt: how to store media file in another database without changing setting

Title: How to add new fields in django user model [closed]
URL:https://stackoverflow.com/questions/54490783/how-to-add-new-fields-in-django-user-model
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .cloud_storage import GoogleCloudMediaStorage
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class AdminAccount(models.Model):
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.email
    
class Lost_Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
    date_uploaded = models.DateTimeField(default=timezone.now)
    item_image = models.ImageField(upload_to="images/",storage=GoogleCloudMediaStorage(), null=True,blank=True )
    image_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=1000, default='',blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()