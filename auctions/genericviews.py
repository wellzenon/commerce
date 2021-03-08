from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Listing
from django import forms
from django.views import generic

class NewListingForm(forms.Form):
    title = forms.CharField(label='Enter the title of the listing')
    description = forms.CharField(label='Enter a brief description of the listing')
    start_bid = forms.DecimalField(max_digits=20, decimal_places=2, label='Enter the starting bid value')
    image = forms.URLField(required=False, label="Enter bid's image URL")
    category = forms.ModelChoiceField(Category.objects.all(), required=False)

class ListingListView(generic.ListView):
    model = Listing

def listing_create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            owner = request.user

            l = Listing(title = title, description = description, start_bid = start_bid, image = image, category = category, owner = owner)
            l.save()

            return HttpResponseRedirect(reverse("listing-list"))
        else:
            return render(request, "auctions/listing-create.html", {
                'form': form,
                'message': 'Invalid data'
            })
    else:
        return render(request, "auctions/listing-create.html", {
            'form': NewListingForm(),
        })