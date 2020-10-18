from django.contrib import admin

from .models import Bid, Auction, Comment, Category, User, Photo, WatchList
# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id","name","price","current_bid","creation_date","auction_category")

#class AuctionAdmin(admin.ModelAdmin):
#    filter_horizontal = ("photos",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("id","price","auction_bid","auctioner")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","commenter","comment_to","text")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id","image_name","url")

class WatchAdmin(admin.ModelAdmin):
   filter_horizontal = ()


admin.site.register(Bid,BidAdmin)
admin.site.register(Auction,AuctionAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Photo,PhotoAdmin)
admin.site.register(WatchList,WatchAdmin)
admin.site.register(User)
