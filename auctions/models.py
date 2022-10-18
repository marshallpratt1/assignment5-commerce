from email.mime import image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    
    def __str__(self):
        return f'{self.title}, price: ${self.price}'

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    bid_time = models.DateTimeField(auto_now_add=True)
    bid_amount = models.IntegerField()

class Comment(models.Model):
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField()

class Watchlist(models.Model):
    watchlist_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist")
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")