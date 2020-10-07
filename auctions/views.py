from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import User, Auction, Category, Bid, Comment

class EntityForm(forms.Form):
    name = forms.CharField(label = "name")
    price = forms.CharField(label= "price")
    category = forms.CharField(label= "category")

def index(request):
    return render(request, "auctions/index.html",{
        "auctions":Auction.objects.all()
    })

def create(request):
    if request.method == "POST":
        form = EntityForm(request.POST)
        message=""
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            date = datetime.now()
            category = form.cleaned_data["category"]
        else:
            message = "Invalid form... Try again."
            return render(request,"auctions/create.html",{
                "form":form,
                "message":message
            })
        get_pk = Auction.objects.order_by('-pk')[0]
        last_pk = get_pk.pk +1
        new_auction = Auction(last_pk,name,price,date,category)
        new_auction.save()

    return render(request, "auctions/create.html",{
        "categories": Category.objects.all(),
    })

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
