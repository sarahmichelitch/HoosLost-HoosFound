"""
REFERENCES:

Title: Upload Images To Django - Django Wednesdays #38
URL: https://www.youtube.com/watch?v=O5YkEFLXcRg&ab_channel=Codemy.com

Title: Working with Forms
URL: https://docs.djangoproject.com/en/4.2/topics/forms/
"""

from django import forms
from .models import Lost_Item
from django.contrib.auth.models import User
from .models import UserProfile
class UploadItemForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput())
    item_image = forms.ImageField(required=False)
    class Meta:
        model = Lost_Item
        fields = ['name', 'location', 'latitude', 'longitude', 'item_image','description']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'item-input',
                'placeholder': 'enter item'
            }),
            'location': forms.TextInput(attrs={
                'id': 'location-input',
                'placeholder': 'enter location',
            }),
            'description': forms.Textarea(attrs={
                'id': 'description-input',
                'placeholder': 'Enter description up to 1000 characters',
                'rows': 3,
                'maxlength': '1000', 
            }),
        }
        labels = {
            'name': 'Item',
            'location': 'Location',
            'item_image': 'Image',
            'description': 'Description',
        }
        
class ChangeUsername(forms.Form):
    new_username = forms.CharField(max_length=150, required=True)
    
class ChangePhonenum(forms.ModelForm):
    class Meta:
        model = UserProfile  
        fields = ['phone_number']  

