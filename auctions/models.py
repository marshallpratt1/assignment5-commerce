from email.mime import image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField()
    
    def __str__(self):
        return f'{self.title}, price: ${self.price}'

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_maker")
    bid_time = models.DateTimeField(auto_now_add=True)
    bid = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()