from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.create_listing, name="create_listing"),
    path("Categories/<str:chosen_category>", views.categories_view, name="categories"),
    path("Watchlist", views.watchlist, name="watchlist"),
    path("MyListings", views.my_listings, name="my_listings"),
    path("MyWins", views.my_wins, name="my_wins"),
    path("EditListing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("Listing/<int:listing_id>", views.listing, name="listing"),
    path("api/status", views.api_status, name="api-status"),
    path("api/watchlist/<int:listing_id>", views.api_watchlist, name="api-watchlist"),
]
