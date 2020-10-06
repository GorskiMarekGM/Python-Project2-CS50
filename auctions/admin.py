from django.contrib import admin

from .models import Bid, Auction, Comment, Category, User
# Register your models here.

admin.site.register(Bid)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)
