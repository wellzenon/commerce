from django import views
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User, Bid, Comment

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

def index(request):
    context={}
    context['listing_list'] = Listing.objects.filter(closed=None)
    if request.user.is_authenticated:
        if request.user.winners.all():
            context['win_count'] = request.user.winners.count()
        else:
            context.pop('win_count', None)
    return render(request, "auctions/index.html",context)

def closed(request):
    listing_list = Listing.objects.exclude(closed=None)
    return render(request, "auctions/index.html",{
        'listing_list': listing_list
    })

def won(request):
    listing_list = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/index.html",{
        'listing_list': listing_list
    })

def listing_to_context(request, pk):
    listing = Listing.objects.get(pk=pk)
    context = vars(listing)
    context['category'] = listing.category.all()
    context['category_list'] = Category.objects.all()
    context['owner'] = listing.owner
    context['current_price'] = listing.current_price
    context['history'] = listing.history
    if request.user.is_active:
        context['listing_in_watchlist'] = listing in request.user.watchlist.all()
    return context


def listing(request, pk):
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)
    
@login_required
def create(request):
    if request.method == 'POST':
        owner = request.user
        title = request.POST['title']
        description = request.POST["description"]
        start_bid = float(request.POST["start_bid"])
        image = request.POST["image"]
        l = Listing(
                title = title, 
                description = description, 
                start_bid = start_bid, 
                image = image, 
                owner = owner
            )
        try:
            l.save()
            if "category" in request.POST:
                category = Category.objects.filter(pk__in=request.POST.getlist("category"))
                l.category.set(category)
        except:
            return render(request, 'auctions/create.html', {
                'title': title,
                'description': description,
                'start_bid': start_bid,
                'image': image,
                'category': category,
                'message': "Can't save.",
            })
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/create.html',{
            'category_list':Category.objects.all(),
        })
    
@login_required
def edit(request, pk):
    listing = Listing.objects.get(pk=pk)
    if request.user == listing.owner:
        if request.method == 'POST':            
            listing.title = request.POST['title']
            listing.description = request.POST["description"]
            listing.start_bid = float(request.POST["start_bid"])
            listing.image = request.POST["image"]
            listing.save()
            if "category" in request.POST:
                listing.category.set(Category.objects.filter(pk__in=request.POST.getlist("category")))
            else:
                listing.category.clear()
            context = listing_to_context(request, pk)
            return render(request, 'auctions/listing.html', context)
        else:
            context = listing_to_context(request, pk)
            return render(request, 'auctions/edit.html', context)
    else:
        return render(request, 'auctions/listing.html', listing_to_context(request, pk))

@login_required
def close(request, pk):
    listing = Listing.objects.get(pk=pk)
    if not listing.closed and listing.owner == request.user:
        listing.close()
        listing.save()
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)

@login_required
def open(request, pk):
    listing = Listing.objects.get(pk=pk)
    if listing.closed and listing.owner == request.user:
        listing.open()
        listing.save()
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)

def remove_listing_from_watchlist(request, pk):
    owner = request.user
    listing = Listing.objects.get(pk=pk)
    owner.watchlist.remove(listing)

@login_required
def watchlist(request):
    owner = request.user
    context = { 'watchlist': owner.watchlist.all() }
    return render(request, 'auctions/watchlist.html', context)

def watchlist_listing(request, pk):
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)

@login_required
def watchlist_add(request, pk):
    owner = request.user
    listing = Listing.objects.get(pk=pk)
    owner.watchlist.add(listing)
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)

@login_required
def watchlist_remove_from_watchlist(request, pk):
    watchlist_remove(request, pk)
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist_remove(request, pk):
    remove_listing_from_watchlist(request, pk)
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        'categories': categories
    })

def category(request, pk):
    category = Category.objects.get(pk=pk)
    listing_list = Listing.objects.filter(category=pk)

    return render(request, "auctions/category.html",{
        'category': category,
        'listing_list': listing_list
    })

@login_required
def bid(request, pk):
    listing = Listing.objects.get(pk=pk)
    context = {}
    if request.POST['bid'] == '':
        value = 0
    else:
        value = float(request.POST['bid'])    
    if request.method == 'POST':
        if listing.closed:
            context.update({'message': "Listing is closed"})
        elif listing.current_price == listing.start_bid > value or listing.start_bid < listing.current_price >= value:
            context.update({'message': "Bid value must be over current price"})
        else:
            listing = Listing.objects.get(pk=pk)
            bid = Bid(owner=request.user, listing=listing, value=value)
            bid.save()
    context.update(listing_to_context(request, pk))
    return render(request, 'auctions/listing.html', context)

@login_required
def comment(request, pk):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=pk)
        comment = Comment(listing=listing, text=request.POST['comment'], owner=request.user)
        comment.save()
    context = listing_to_context(request, pk)
    return render(request, 'auctions/listing.html', context)