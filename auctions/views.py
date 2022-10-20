from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import *
from django.contrib import messages
from .models import *
from datetime import timedelta, date


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


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


def create_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():            
            listing_title = request.POST["title"]
            listing_price = request.POST["price"]
            listing_description = request.POST["description"]
            listing_image = request.FILES["image"]
            listing_category = request.POST["category"]
            listing = Listing(listing_user=request.user, title=listing_title, price=listing_price, description=listing_description,
                                image=listing_image, category=listing_category, end_date=date.today()+timedelta(days=7))
            listing.save()
            return redirect("listing", listing_id = listing.id)
        else:
            messages.error(request, 'Something went wrong')
            return render(request, "auctions/create_listing.html", {"form": NewListing()})
    else:
        return render(request, "auctions/create_listing.html", {"form": NewListing()})

def edit_listing(request, listing_id):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(id=listing_id)            
            listing_title = request.POST["title"]
            listing_price = request.POST["price"]
            listing_description = request.POST["description"]
            if request.FILES.get("image"):
                listing.image.delete()
                listing_image = request.FILES["image"]
            else: listing_image = listing.image
            listing_category = request.POST["category"]
            listing.delete()
            listing = Listing(listing_user=request.user, title=listing_title, price=listing_price, description=listing_description,
                                image=listing_image, category=listing_category, end_date=date.today()+timedelta(days=7))
            listing.save()
            return redirect("listing", listing_id = listing.id)
    else:        
        listing = Listing.objects.get(id=listing_id)
        form = NewListing(initial={
            'title': listing.title,
            'price': listing.price,
            'description': listing.description,
            'image': listing.image,
            'category': listing.category,
        })
        return render(request, "auctions/create_listing.html", {"form": form})

def listing(request, listing_id):
    if request.method == "POST":
        if request.POST.get("delete"):
            listing = Listing.objects.get(id=listing_id)
            listing.image.delete()
            listing.delete()
            return redirect("index")
        elif request.POST.get("edit"):
            return redirect("edit_listing", listing_id)
        elif request.POST.get("watchlist"):
            watch = Watchlist()
            watch.watchlist_listing = Listing.objects.get(id=listing_id)
            watch.watchlist_user = request.user
            watch.save()            
            return render(request, 'auctions/listing.html', {
            "listing": Listing.objects.get(id=listing_id),
            "watchlist": True,
            })
        elif request.POST.get("remove_watchlist"):
            watchlist = Watchlist.objects.filter(
                    watchlist_listing = listing_id,
                    watchlist_user = User.objects.get(id=request.user.id)
            ).first()
            watchlist.delete()
            return render(request, 'auctions/listing.html', {
            "listing": Listing.objects.get(id=listing_id),
            "watchlist": False,
            })

    else:
        try:        
            listing = Listing.objects.get(id=listing_id)
        except:
            messages.error(request, "Cannot find that listing.")
        if request.user.is_authenticated:
            watchlist = Watchlist.objects.filter(
                    watchlist_listing = listing_id,
                    watchlist_user = User.objects.get(id=request.user.id)
            ).first()
        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": watchlist,
            })