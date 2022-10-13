from django import forms


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
    category = forms.CharField(label="Category", widget=forms.Select(choices=categories))
    description = forms.CharField(label="Entry:", widget=forms.Textarea())
    image = forms.FileField(label="Image:", required=False)