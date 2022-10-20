from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *


class NewListing(forms.Form):    
    categories = [
        ('other', 'Other'),
        ('furniture', 'Furniture'),
        ('outdoor', 'Outdoor'),
        ('sports', 'Sports'),
        ('automobile', 'Automobile'),
        ('bicycle', 'Bicycle'),
        ('apparel', 'Apparel'),
        ('electronics', 'Electronics'),
    ]
 
    title = forms.CharField(label="Title:")    
    price = forms.IntegerField(label="Price:", min_value=0)    
    description = forms.CharField(label="Entry:", widget=forms.Textarea())
    image = forms.ImageField(label="Image:", required=False)   
    category = forms.CharField(label="Category", widget=forms.Select(choices=categories))