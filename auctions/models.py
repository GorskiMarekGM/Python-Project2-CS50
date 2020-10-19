from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Photo(models.Model):
    image_name = models.TextField()
    url = models.TextField()

    def __str__(self):
        return f"{self.url}"


class Auction(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    current_bid = models.IntegerField()
    creation_date = models.DateTimeField()
    available = models.BooleanField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    photos = models.ManyToManyField(Photo, related_name='photos', blank=True)
    auction_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="creator")

    def __str__(self):
        return f"{self.id} {self.name}"


class Bid(models.Model):
    price = models.IntegerField()
    auction_bid = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    auctioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioner")

    def __str__(self):
        return f"{self.price}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_to = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")
    text = models.TextField()

    def __str__(self):
        return f"{self.commenter} {self.comment_to} {self.text}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    auctions = models.ManyToManyField(Auction, related_name="auctions", blank=True)
    
    def __str__(self):
        return f"{self.user}'s watchlist'"