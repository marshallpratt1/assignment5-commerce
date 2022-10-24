from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *


class NewListing(forms.Form):    
    categories = [
        ('Other', 'Other'),
        ('Furniture', 'Furniture'),
        ('Outdoor', 'Outdoor'),
        ('Sports', 'Sports'),
        ('Automobile', 'Automobile'),
        ('Bicycles', 'Bicycle'),
        ('Apparel', 'Apparel'),
        ('Electronics', 'Electronics'),
    ]
 
    title = forms.CharField(label="Title:")    
    price = forms.IntegerField(label="Price:", min_value=0)    
    description = forms.CharField(label="Entry:", widget=forms.Textarea())
    image = forms.ImageField(label="Image:", required=False)   
    category = forms.CharField(label="Category", widget=forms.Select(choices=categories))


class CommentForm(forms.Form):
    comment = forms.CharField(label="New Comment:", widget=forms.Textarea())