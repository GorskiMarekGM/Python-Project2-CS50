from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories_choose, name="categories_choose"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:auction_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:auction_id>", views.watchlist_remove, name="watchlist_remove"),
    path("create", views.create, name="create"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
