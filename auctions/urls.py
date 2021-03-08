from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("", views.index, name="index"),
    path("closed/", views.closed, name="closed"),
    path("won/", views.won, name="won"),

    path("create/", views.create, name="create"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("listing/<int:pk>/edit", views.edit, name="edit"),
    path("listing/<int:pk>/close", views.close, name="close"),
    path("listing/<int:pk>/open", views.open, name="open"),
    path("listing/<int:pk>/bid", views.bid, name="bid"),
    path("listing/<int:pk>/comment", views.comment, name="comment"),

    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<int:pk>", views.watchlist_listing, name="watchlist-listing"),
    path("listing/<int:pk>/add", views.watchlist_add, name="watchlist-add"),
    path("listing/<int:pk>/remove", views.watchlist_remove, name="watchlist-remove"),
    path("watchlist/<int:pk>/remove", views.watchlist_remove_from_watchlist, name="watchlist-remove-from-watchlist"),

    path("categories/", views.categories, name="categories"),
    path("category/<int:pk>", views.category, name="category"),
]