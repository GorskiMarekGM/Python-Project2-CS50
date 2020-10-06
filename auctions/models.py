from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

class Auction(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(max_length=10)
    creation_date = models.TimeField()
    auction_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.id}"

class Bid(models.Model):
    price = models.IntegerField()
    auction_bid = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    auctioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioner")

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_to = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")
    text = models.TextField()
