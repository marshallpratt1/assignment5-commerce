from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import *
from django.contrib import messages
from .models import *
from datetime import timedelta, date


#display active listings, retrieve user's watchlist status
#TODO: update Watchlist model to be able to use related_name
def index(request):
    listings = Listing.objects.filter(closed=False)
    if listings.count == 0: listings = False
    watched_listings = []
    if request.user.is_authenticated:
        watched = Watchlist.objects.filter(watchlist_user=request.user)        
        for i in watched:
            watched_listings.append(i.watchlist_listing)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist": watched_listings, 
    })

#provided login 
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

#provided logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#provided register
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

#displays only active categories
#TODO: update models to handle this more efficiently
def categories_view(request, chosen_category):
    if chosen_category == 'All':
        categories = []
        listings = Listing.objects.all()
        for listing in listings:
            if listing.category not in categories:
                categories.append(listing.category)
        if len(categories) == 0: categories = False
        return render(request, 'auctions/categories.html', {"categories":categories,
                                                            "All": True})
    else:
        watched_listings = []
        if request.user.is_authenticated:
            watched = Watchlist.objects.filter(watchlist_user=request.user)        
            for i in watched:
                watched_listings.append(i.watchlist_listing)
        listings = Listing.objects.filter(category=chosen_category)
        return render(request, 'auctions/categories.html', {"listings":listings,
                                                            "All": False,
                                                            "category": chosen_category,
                                                            "watchlist": watched_listings,})

#display user's wathced listings, retrieve user's watchlist status
#TODO: update Watchlist model to be able to use related_name
def watchlist(request):
    listings=[]
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(watchlist_user=request.user)
        for item in user_watchlist:
            listings.append(item.watchlist_listing)
    if len(listings)==0: listings=False
    return render(request, 'auctions/watchlist.html', {"listings": listings})

#only active users can create a listing
def create_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():            
            listing_title = request.POST["title"]
            listing_price = request.POST["price"]
            listing_description = request.POST["description"]
            if request.FILES.get("image"): listing_image = request.FILES["image"]
            else: listing_image = False
            listing_category = request.POST["category"]
            listing = Listing(listing_user=request.user, title=listing_title, price=listing_price, 
                                description=listing_description, image=listing_image, closed=False,
                                category=listing_category, end_date=date.today()+timedelta(days=7))
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
                                image=listing_image, category=listing_category, closed=False,end_date=date.today()+timedelta(days=7))
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

def my_listings(request):
    listings = Listing.objects.filter(listing_user = request.user)
    if len(listings)==0:listings=False
    return render(request, "auctions/my_listings.html", {"listings": listings})

def my_wins(request):
    listings = Listing.objects.filter(highest_bidder = request.user, closed=True)
    if len(listings)==0:listings=False
    return render(request, "auctions/won_auctions.html", {"listings": listings})

#handles all  action on listing page
#TODO: this function is pretty fat, look into ways to trim this down
def listing(request, listing_id):
    #listing globals:
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
                        watchlist_listing = listing_id,
                        watchlist_user = User.objects.get(id=request.user.id)
                ).first()
    comment_form = CommentForm()
    comments = Comment.objects.filter(comment_listing = listing_id)
    try: listing = Listing.objects.get(id=listing_id)
    except: messages.error(request, "Cannot find that listing.")
    if comments.count == 0: comments = False

    if request.method == "POST":
    #handle submit button actions
        if request.POST.get("make_bid"):
            bid = Bid(listing=Listing.objects.get(id=listing_id),
                    bid_user=request.user,
                    bid_amount=request.POST["bid_amount"])
            bid.save()
            listing.price = request.POST["bid_amount"]
            listing.highest_bidder=request.user
            listing.save()
            #add to watchlist if not already
            Watchlist.objects.get_or_create(watchlist_listing=listing, watchlist_user=request.user)
            return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": True,
            "comments": comments,
            "comment_form": comment_form,
            })

        if request.POST.get("close_auction"):
            listing.closed=True
            listing.save()
            return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "comment_form": comment_form,
            })

        if request.POST.get("delete"):
            listing = Listing.objects.get(id=listing_id)
            listing.image.delete()
            listing.delete()
            return redirect("index")

        elif request.POST.get("edit"):
            return redirect("edit_listing", listing_id)

        elif request.POST.get("make_comment"):
            comment_form = CommentForm(request.POST)
            new_comment = Comment(
                comment_user = User.objects.get(id=request.user.id),
                comment_listing = listing,
                comment = request.POST["comment"],
                )
            new_comment.save()
            return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "comment_form": CommentForm(),
            })
            
        elif request.POST.get("delete_comment"):
            Comment.objects.get(id=request.POST["comment_id"]).delete()
            return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "comment_form": CommentForm(),
            })

    else: 
    #this is a listing view request
    #check for user authentication prior to assiginiong watchlist
        
        if request.user.is_authenticated:
            pass
        else: watchlist = False        

        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "comment_form": comment_form,
            })

from django.http import JsonResponse
def api_status(request):
    status = {
        'total_listings': Listing.objects.all().count(),
        'active_listings': Listing.objects.filter(closed=False).count(),      
        'watched_listings': Watchlist.objects.filter(watchlist_user=request.user).count(),  
    }
    return JsonResponse(status)


#ask about the convention for writing a data input
def api_toggle_watchlist(request, listing_id):
    watch, created = Watchlist.objects.get_or_create(
        watchlist_listing = Listing.objects.get(id=listing_id),
        watchlist_user = request.user
    )
    if not created: watch.delete()
    return JsonResponse({
        'watched_listings': Watchlist.objects.filter(watchlist_user=request.user).count(),  
    })