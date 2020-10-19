from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Max

from .models import User, Auction, Category, Bid, Comment, Photo, WatchList

class EntityForm(forms.Form):
    name = forms.CharField(label = "name")
    price = forms.CharField(label= "price")
    category = forms.CharField(label= "category")

class WatchList_Id(forms.Form):
    WatchList_Id = forms.IntegerField(label="id")

class BidForm(forms.Form):
    price = forms.IntegerField(label="price")
    

def index(request):
    return render(request, "auctions/index.html",{
        "auctions":Auction.objects.all(),
        "photos":Photo.objects.all(),
    })

def getLastPk(obj):
    if(obj.objects.first() is None):
        return 1
    else:
        get_pk = obj.objects.order_by('-pk')[0]
        last_pk = get_pk.pk +1
        return last_pk

def listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html",{
        "listing":listing,
        "photos":Photo.objects.all(),
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories":Category.objects.all(),
    })

def categories_choose(request,category_id):
    auctions_by_cat = Auction.objects.filter(auction_category=category_id)

    return render(request, "auctions/index.html",{
        "auctions":auctions_by_cat,
        "photos":Photo.objects.all(),
    })

def close(request,listing_id):
    auction = Auction.objects.get(pk=listing_id)
    bids = Bid.objects.filter(auction_bid=auction)
    max_price = bids.order_by('-price')[0]
    winner = User
    
    for bid in bids:
        if bid.price == max_price.price:
            winner = bid.auctioner
            auction.winner = winner
            auction.available = False
            auction.save()

    return render(request, "auctions/close.html",{
        "max_price": max_price,
        "winner":winner
    })

def bid(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            form = BidForm(request.POST)
            bid_price = int(form.data["bid"])
            auction_id = form.data["auction_id"]
            auction = Auction.objects.get(pk=auction_id)
            auction_bid = auction.current_bid
            auction_price = auction.price

            message =""
            
            listing = Auction.objects.get(pk=auction_id)

            if(bid_price > auction_price):
                if (bid_price > auction_bid):
                    auction.current_bid = bid_price
                    auction.save()

                    bid_obj = Bid(id = getLastPk(Bid),price = bid_price, auction_bid = auction, auctioner = request.user)
                    bid_obj.save()

                    messages.add_message(request, messages.INFO, "Successfully placed bid")
            else:
                messages.add_message(request, messages.INFO, "Your bid is lower then current value") 

            return redirect('listing', listing_id = auction_id)


    else:
        messages.add_message(request, messages.INFO, "you are not authenticated") 
        return index

def watchlist(request):
    watchlist = WatchList.objects.get(user = request.user)

    return render(request, "auctions/watchlist.html",{
        "watch_list" : watchlist.auctions.all(),
    })

def watchlist_add(request, auction_id):
    if request.user.is_authenticated:

        if WatchList.objects.filter(user=request.user).exists():
            watchlist = WatchList.objects.get(user = request.user)
        else:
            watchlist = WatchList(id = getLastPk(WatchList),user = request.user)

        auction_to_save = Auction.objects.get(id=auction_id)    
        watchlist.save()
        watchlist.auctions.add(auction_to_save)
        watchlist.save()

    return render(request, "auctions/watchlist.html",{
        "watch_list" : watchlist.auctions.all(),
    })

def watchlist_remove(request, auction_id):
    if request.user.is_authenticated:
        user = request.user
        user_watchlist = WatchList.objects.filter(user=user)[0]

        user_watchlist.auctions.filter(id=auction_id).delete()

    return redirect('watchlist')

def create(request):
    if request.method == "POST":
        form = EntityForm(request.POST)
        message=""
        #checks if img exists
        is_img_set = request.FILES.get('img', False)
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            date = datetime.now()
            category = form.cleaned_data["category"]
            category_obj = Category.objects.get(pk=category)

            if(is_img_set):
                photo = upload(request)

        else:
            message = "Invalid form... Try again."
            return render(request,"auctions/create.html",{
                "form":form,
                "message":message
            })
            
        new_auction = Auction(id = getLastPk(Auction),name = name,price = price,current_bid = 0,creation_date = date,auction_category = category_obj, available = True, creator= request.user)
        #new_auction.creator = request.user
        #new_auction.available = True
        new_auction.save()

        if(is_img_set):
            new_auction.photos.add(photo)
            new_auction.save()
        return redirect('index')
        

    return render(request, "auctions/create.html",{
        "categories": Category.objects.all(),
    })



def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['img']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        
        photo = Photo(getLastPk(Photo),uploaded_file.name,url)
        photo.save()

        return photo

#-------LOGIN PART------------
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
