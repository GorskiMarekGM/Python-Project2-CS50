from django.contrib import admin

from .models import Bid, Auction, Comment, Category, User
# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id","name","price","auction_category")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id","price","auction_bid","auctioner")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","commenter","comment_to","text")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")


admin.site.register(Bid,BidAdmin)
admin.site.register(Auction,AuctionAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
